from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    TYPE_CHOICES = [
        ('class', 'Class Reminder'),
        ('attendance', 'Attendance Alert'),
        ('event', 'Campus Event'),
        ('exam', 'Exam Notification'),
        ('system', 'System Announcement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='class')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type.upper()}] {self.title}"

class StudyPartnerRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Request'),
        ('accepted', 'Connected'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_partner_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partner_requests')
    subject_or_goal = models.CharField(max_length=150, help_text="e.g. DSA in Python, Gate Prep, Cloud Computing")
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.subject_or_goal})"
