from django.db import models
from django.contrib.auth.models import User

class StudyDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='study_documents')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, default="Computer Science")
    file = models.FileField(upload_to='study_docs/', null=True, blank=True)
    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    page_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='flashcards')
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, null=True, blank=True, related_name='flashcards')
    front = models.TextField()
    back = models.TextField()
    is_mastered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Card: {self.front[:30]}..."

class QuizQuestion(models.Model):
    document = models.ForeignKey(StudyDocument, on_delete=models.CASCADE, null=True, blank=True, related_name='quizzes')
    question = models.TextField()
    options = models.JSONField(default=list)  # 4 choices
    correct_index = models.IntegerField(default=0)
    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"Q: {self.question[:40]}..."
