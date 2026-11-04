from django.db import models
from django.contrib.auth.models import User

class CareerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='career_profile')
    target_role = models.CharField(max_length=100, default="Full Stack AI Engineer")
    target_companies = models.CharField(max_length=200, default="Microsoft, Google, Amazon, Cognizant, Palo Alto")
    skills = models.JSONField(default=list)  # e.g. ["Python", "React Native", "Django", "SQL", "Git"]
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    resume_score = models.IntegerField(default=78)
    resume_analysis = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.target_role}"

class InterviewQuestion(models.Model):
    TYPE_CHOICES = [
        ('hr', 'HR & Behavioral'),
        ('technical', 'Technical Core'),
        ('dsa', 'Data Structures & Algorithms'),
    ]

    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='technical')
    role_category = models.CharField(max_length=100, default="Software Engineering")
    question = models.TextField()
    sample_answer = models.TextField()
    tips = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, default="Medium")

    def __str__(self):
        return f"[{self.question_type.upper()}] {self.question[:40]}..."
