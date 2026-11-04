from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import CareerProfile, InterviewQuestion
from .serializers import CareerProfileSerializer, InterviewQuestionSerializer
from services.gemini_service import gemini_service
from study_assistant.pdf_processor import extract_text_from_pdf

class CareerProfileView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            profile, _ = CareerProfile.objects.get_or_create(
                user=request.user,
                defaults={'skills': ['Python', 'JavaScript', 'SQL', 'Git', 'Data Structures']}
            )
            return Response(CareerProfileSerializer(profile).data)
        
        # Default mock profile for guest preview
        return Response({
            'target_role': 'Full Stack AI Engineer',
            'target_companies': 'Microsoft, Google, Cognizant, Palo Alto',
            'skills': ['Python', 'React Native', 'Django', 'REST APIs', 'SQL'],
            'resume_score': 84,
            'resume_analysis': {
                'score': 84,
                'strengths': [
                    'Solid grasp of full stack architectural patterns.',
                    'Practical project work using modern mobile and backend frameworks.',
                    'Clear academic standing at Lovely Professional University.'
                ],
                'improvements': [
                    'Include deployment metrics and containerization (Docker).',
                    'Highlight performance optimization numbers.'
                ],
                'recommended_projects': [
                    'Multi-tenant Campus RAG Assistant with Gemini',
                    'High-concurrency Task Orchestrator'
                ],
                'keywords_to_add': ['System Architecture', 'CI/CD Pipelines', 'Docker', 'RESTful API']
            }
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'message': 'Profile saved locally'})

        profile, _ = CareerProfile.objects.get_or_create(user=request.user)
        if 'target_role' in request.data:
            profile.target_role = request.data['target_role']
        if 'target_companies' in request.data:
            profile.target_companies = request.data['target_companies']
        if 'skills' in request.data:
            profile.skills = request.data['skills']
        profile.save()
        return Response(CareerProfileSerializer(profile).data)

class ResumeAnalyzeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        file = request.FILES.get('resume')
        text = request.data.get('resume_text', '')
        role = request.data.get('target_role', 'Software Engineer')

        resume_content = text
        if file:
            if file.name.lower().endswith('.pdf'):
                resume_content, _ = extract_text_from_pdf(file)
            else:
                try:
                    resume_content = file.read().decode('utf-8', errors='ignore')
                except Exception:
                    resume_content = f"Uploaded resume: {file.name}"

        if not resume_content:
            resume_content = "Computer Science student at LPU with experience in Python, Web Development, and Data Structures."

        analysis = gemini_service.analyze_resume(resume_content, career_goal=role)

        if request.user.is_authenticated:
            profile, _ = CareerProfile.objects.get_or_create(user=request.user)
            profile.resume_score = analysis.get('score', 80)
            profile.resume_analysis = analysis
            if file:
                profile.resume_file = file
            profile.save()

        return Response({
            'analysis': analysis,
            'message': 'Resume evaluated successfully by Gemini Career Engine.'
        })

class InterviewQuestionsListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        q_type = request.query_params.get('type')  # 'hr', 'technical', 'dsa'
        qs = InterviewQuestion.objects.all()
        if q_type and q_type != 'all':
            qs = qs.filter(question_type=q_type)
        return Response(InterviewQuestionSerializer(qs, many=True).data)

class PersonalizedRoadmapView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        role = request.query_params.get('role', 'Full Stack AI Engineer')
        
        # 8-week structured placement preparation roadmap
        roadmap = [
            {
                "week": 1,
                "title": "Data Structures Foundations",
                "focus": "Arrays, Strings, Two Pointers & Hash Maps",
                "milestone": "Solve 20 LeetCode Easy/Medium problems",
                "hours": "12 hrs"
            },
            {
                "week": 2,
                "title": "Linked Lists & Stacks/Queues",
                "focus": "Monotonic stacks, slow/fast pointers, circular queues",
                "milestone": "Implement LRU Cache & Min Stack from scratch",
                "hours": "14 hrs"
            },
            {
                "week": 3,
                "title": "Trees, BST & Heaps",
                "focus": "Tree traversals, Lowest Common Ancestor, Top-K elements",
                "milestone": "Master recursion and tree serializations",
                "hours": "15 hrs"
            },
            {
                "week": 4,
                "title": "Graphs & Dynamic Programming I",
                "focus": "BFS, DFS, Dijkstra, Memoization vs Tabulation (0/1 Knapsack)",
                "milestone": "Solve classic coin change & longest common subsequence",
                "hours": "18 hrs"
            },
            {
                "week": 5,
                "title": "Backend Engineering & REST APIs",
                "focus": "Django/FastAPI, MySQL indexing, ACID transactions, JWT Auth",
                "milestone": "Build rate-limited secure RESTful microservice",
                "hours": "14 hrs"
            },
            {
                "week": 6,
                "title": "Mobile & Frontend Systems",
                "focus": "React Native, Expo, State Management, Offline Caching",
                "milestone": "Build complete CampusGPT mobile screen workflows",
                "hours": "16 hrs"
            },
            {
                "week": 7,
                "title": "System Design & Cloud Basics",
                "focus": "Load balancing, horizontal scaling, caching strategies, Docker",
                "milestone": "Design scalable WhatsApp / Uber backend on whiteboard",
                "hours": "12 hrs"
            },
            {
                "week": 8,
                "title": "Mock Interviews & Placement Readiness",
                "focus": "LPU PRT mock drives, HR STAR method, company-specific rounds",
                "milestone": "3 technical and 2 HR mock interviews completed",
                "hours": "10 hrs"
            }
        ]
        return Response({'role': role, 'roadmap': roadmap})
