from django.urls import path
from .views import (
    CareerProfileView, ResumeAnalyzeView,
    InterviewQuestionsListView, PersonalizedRoadmapView
)

urlpatterns = [
    path('profile/', CareerProfileView.as_view(), name='career-profile'),
    path('resume-analyze/', ResumeAnalyzeView.as_view(), name='career-resume-analyze'),
    path('interview-questions/', InterviewQuestionsListView.as_view(), name='career-interview-questions'),
    path('roadmap/', PersonalizedRoadmapView.as_view(), name='career-roadmap'),
]
