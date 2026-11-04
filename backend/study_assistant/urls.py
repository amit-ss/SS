from django.urls import path
from .views import (
    DocumentUploadView, DocumentListView, SummarizeTextView,
    GenerateMCQsView, GenerateFlashcardsView, ProblemSolverView,
    FlashcardListView
)

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='study-upload'),
    path('documents/', DocumentListView.as_view(), name='study-documents'),
    path('summarize/', SummarizeTextView.as_view(), name='study-summarize'),
    path('generate-mcqs/', GenerateMCQsView.as_view(), name='study-generate-mcqs'),
    path('generate-flashcards/', GenerateFlashcardsView.as_view(), name='study-generate-flashcards'),
    path('solve-problem/', ProblemSolverView.as_view(), name='study-solve-problem'),
    path('flashcards/', FlashcardListView.as_view(), name='study-flashcards'),
]
