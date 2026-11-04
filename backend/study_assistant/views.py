from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import StudyDocument, Flashcard, QuizQuestion
from .serializers import StudyDocumentSerializer, FlashcardSerializer, QuizQuestionSerializer
from .pdf_processor import extract_text_from_pdf
from services.gemini_service import gemini_service

class DocumentUploadView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        file = request.FILES.get('file')
        title = request.data.get('title', 'Study Notes').strip()
        subject = request.data.get('subject', 'General Academics').strip()
        direct_text = request.data.get('text', '').strip()

        extracted_text = direct_text
        page_count = 1

        if file:
            filename = file.name.lower()
            if filename.endswith('.pdf'):
                extracted_text, page_count = extract_text_from_pdf(file)
            else:
                try:
                    extracted_text = file.read().decode('utf-8', errors='ignore')
                except Exception:
                    extracted_text = f"Uploaded file: {file.name}"

        # Generate summary using Gemini AI
        summary = gemini_service.generate_study_summary(extracted_text)

        doc = StudyDocument.objects.create(
            user=request.user if request.user.is_authenticated else None,
            title=title,
            subject=subject,
            file=file,
            extracted_text=extracted_text,
            summary=summary,
            page_count=page_count
        )

        return Response({
            'document': StudyDocumentSerializer(doc).data,
            'message': 'Document uploaded and processed successfully with PyMuPDF and Gemini AI.'
        }, status=status.HTTP_201_CREATED)

class DocumentListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = StudyDocument.objects.all().order_by('-created_at')
    serializer_class = StudyDocumentSerializer

class SummarizeTextView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        text = request.data.get('text', '').strip()
        doc_id = request.data.get('document_id')

        if doc_id:
            doc = StudyDocument.objects.filter(id=doc_id).first()
            if doc:
                text = doc.extracted_text

        if not text:
            return Response({'error': 'No text provided for summarization'}, status=status.HTTP_400_BAD_REQUEST)

        summary = gemini_service.generate_study_summary(text)
        return Response({'summary': summary})

class GenerateMCQsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        text = request.data.get('text', '').strip()
        doc_id = request.data.get('document_id')
        count = int(request.data.get('count', 5))

        if doc_id:
            doc = StudyDocument.objects.filter(id=doc_id).first()
            if doc:
                text = doc.extracted_text

        if not text:
            text = "Operating systems manage CPU scheduling, memory management, and file systems."

        mcqs = gemini_service.generate_mcqs(text, count=count)
        return Response({'mcqs': mcqs})

class GenerateFlashcardsView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        text = request.data.get('text', '').strip()
        doc_id = request.data.get('document_id')

        if doc_id:
            doc = StudyDocument.objects.filter(id=doc_id).first()
            if doc:
                text = doc.extracted_text

        if not text:
            text = "Data structures like hash tables, binary trees, and graphs optimize computation."

        cards_data = gemini_service.generate_flashcards(text)

        # Save flashcards if user is logged in
        saved_cards = []
        for c in cards_data:
            fc = Flashcard.objects.create(
                user=request.user if request.user.is_authenticated else None,
                front=c.get('front', ''),
                back=c.get('back', '')
            )
            saved_cards.append(FlashcardSerializer(fc).data)

        return Response({'flashcards': saved_cards})

class ProblemSolverView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        problem = request.data.get('problem', '').strip()
        subject = request.data.get('subject', 'Engineering/Computer Science').strip()

        if not problem:
            return Response({'error': 'Problem statement is required'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = (f"Act as an expert LPU professor. Solve this academic problem step-by-step with formulas, "
                  f"explanations, and code (if programming related):\n\nSubject: {subject}\nProblem:\n{problem}")

        ai_resp = gemini_service.generate_chat_response(prompt)
        return Response({
            'solution': ai_resp.get('text'),
            'sources': ['AI Step-by-Step Solver']
        })

class FlashcardListView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Flashcard.objects.all().order_by('-created_at')
    serializer_class = FlashcardSerializer
