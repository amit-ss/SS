import json
import os
from pathlib import Path
from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import ChatMessage, KnowledgeDocument
from .serializers import ChatMessageSerializer
from services.gemini_service import gemini_service
from services.llm_service import llm_router

def get_rag_context(query: str) -> tuple[str, list]:
    """Finds relevant LPU documents using keyword and category matching."""
    keywords = [w.lower() for w in query.split() if len(w) > 3]
    matches = []
    
    # Check DB knowledge documents
    docs = KnowledgeDocument.objects.all()
    if docs.exists():
        for doc in docs:
            score = sum(1 for kw in keywords if kw in doc.content.lower() or kw in doc.title.lower())
            if score > 0:
                matches.append((score, doc.content, doc.source_reference))
    
    # If DB is empty, read from lpu_knowledge_base.json
    if not matches:
        json_path = Path(__file__).resolve().parent / 'lpu_knowledge_base.json'
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        score = sum(1 for kw in keywords if kw in item['content'].lower() or kw in item['title'].lower())
                        if score > 0:
                            matches.append((score, item['content'], item['source_reference']))
            except Exception:
                pass

    matches.sort(key=lambda x: x[0], reverse=True)
    top_matches = matches[:2]
    context_text = "\n\n".join([m[1] for m in top_matches])
    sources = list(set([m[2] for m in top_matches]))
    return context_text, sources

class SendMessageView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id', 'default_session').strip()
        provider = (request.data.get('provider') or '').strip().lower() or None

        if not user_message:
            return Response({'error': 'Message cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None

        # 1. Save user message to database
        user_chat = ChatMessage.objects.create(
            user=user,
            role='user',
            content=user_message,
            session_id=session_id
        )

        # 2. Retrieve RAG context from verified LPU sources
        rag_context, sources = get_rag_context(user_message)

        # 3. Retrieve recent conversation history
        past_msgs = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
        history = [{'role': m.role, 'content': m.content} for m in past_msgs]

        # 4. Generate response via GeminiService
        ai_result = gemini_service.generate_chat_response(
            user_message=user_message,
            conversation_history=history,
            rag_context=rag_context,
            provider=provider
        )

        all_sources = list(set(sources + ai_result.get('sources', [])))

        # 5. Save AI response to database
        ai_chat = ChatMessage.objects.create(
            user=user,
            role='ai',
            content=ai_result['text'],
            session_id=session_id,
            sources=all_sources
        )

        # Generate contextual follow-up suggestions
        suggestions = [
            "What is the attendance criteria for exams?",
            "Where is Block 34 located?",
            "Tell me about the Central Library timings",
            "What are the hostel in-time rules?"
        ]

        return Response({
            'message': ChatMessageSerializer(ai_chat).data,
            'model': ai_result.get('model'),
            'provider': ai_result.get('provider'),
            'sources': all_sources,
            'suggestions': suggestions
        })

class ChatHistoryView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = request.query_params.get('session_id', 'default_session')
        messages = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
        return Response(ChatMessageSerializer(messages, many=True).data)

class ClearHistoryView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request):
        session_id = request.query_params.get('session_id', 'default_session')
        ChatMessage.objects.filter(session_id=session_id).delete()
        return Response({'message': 'Conversation history cleared successfully'})

class SuggestedPromptsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'prompts': [
                {"title": "Attendance Policy", "prompt": "What is the minimum attendance requirement at LPU?"},
                {"title": "Central Library", "prompt": "What are the timings and book issue limit for LPU Central Library?"},
                {"title": "Hostel In-time", "prompt": "What are the hostel curfew rules and outing pass process?"},
                {"title": "Placement Eligibility", "prompt": "What are the CGPA and criteria for campus placement drives?"},
                {"title": "Campus Food Hubs", "prompt": "Where can I find food courts and cafes near Block 34 or UniMall?"},
                {"title": "Emergency Hospital", "prompt": "Where is UniHospital located and what is the emergency helpline?"}
            ]
        })

class AIProvidersView(views.APIView):
    """Which AI backends are reachable right now (local Ollama, Ollama Cloud, Gemini)."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'default': llm_router.default_provider(),
            'providers': llm_router.status(),
        })
