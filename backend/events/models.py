from django.db import models
from django.contrib.auth.models import User

class CampusEvent(models.Model):
    CATEGORY_CHOICES = [
        ('hackathon', 'Hackathon & Coding'),
        ('workshop', 'Technical Workshop'),
        ('cultural', 'Cultural Fest & Arts'),
        ('sports', 'Sports & Tournaments'),
        ('seminar', 'Guest Lecture & Seminar'),
        ('placement', 'Placement Drive & Prep'),
    ]

    title = models.CharField(max_length=250)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='hackathon')
    description = models.TextField()
    image_url = models.CharField(max_length=400, blank=True, null=True)
    venue = models.CharField(max_length=150, help_text="e.g. Baldev Raj Mittal Unipolis, Block 34 Audi")
    organizer = models.CharField(max_length=150, default="Student Welfare Organization / Coding Oasis")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_url = models.CharField(max_length=300, blank=True, default="https://ums.lpu.in")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.title} ({self.venue})"

class SavedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_events')
    event = models.ForeignKey(CampusEvent, on_delete=models.CASCADE, related_name='saves')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} saved {self.event.title}"
