from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    reg_number = models.CharField(max_length=20, unique=True, verbose_name="Registration Number")
    course = models.CharField(max_length=100, default="B.Tech Computer Science & Engineering")
    branch = models.CharField(max_length=100, default="CSE")
    semester = models.IntegerField(default=5)
    section = models.CharField(max_length=10, default="K22DF")
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.FileField(upload_to='profiles/', blank=True, null=True)
    dark_mode = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    career_goal = models.CharField(max_length=100, default="Full Stack AI Engineer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.reg_number})"
