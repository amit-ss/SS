from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI Assistant'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, db_index=True)
    sources = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.role.upper()} ({self.session_id}): {self.content[:40]}"

class KnowledgeDocument(models.Model):
    CATEGORY_CHOICES = [
        ('admission', 'Admission & Fees'),
        ('academics', 'Academics & Exams'),
        ('hostel', 'Hostel & Housing'),
        ('facilities', 'Campus Facilities'),
        ('placement', 'Placements & Careers'),
        ('rules', 'University Regulations'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='academics')
    content = models.TextField()
    source_reference = models.CharField(max_length=150, default="LPU Official Regulations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
