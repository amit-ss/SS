import math
from django.db import models
from django.contrib.auth.models import User

class SubjectAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='attendance_records')
    subject_name = models.CharField(max_length=150)
    subject_code = models.CharField(max_length=20)
    total_classes = models.IntegerField(default=30)
    classes_attended = models.IntegerField(default=24)
    target_percentage = models.FloatField(default=75.0)
    faculty_name = models.CharField(max_length=100, blank=True, default="Dr. Amit Sharma")
    last_updated = models.DateTimeField(auto_now=True)

    @property
    def current_percentage(self) -> float:
        if self.total_classes == 0:
            return 100.0
        return round((self.classes_attended / self.total_classes) * 100.0, 1)

    @property
    def classes_needed(self) -> int:
        """Consecutive classes needed to reach target percentage."""
        if self.current_percentage >= self.target_percentage:
            return 0
        target = self.target_percentage
        # (attended + x) / (total + x) >= target / 100
        numerator = (target * self.total_classes) - (100.0 * self.classes_attended)
        denominator = 100.0 - target
        if denominator <= 0:
            return 0
        return max(0, math.ceil(numerator / denominator))

    @property
    def max_missable_classes(self) -> int:
        """Max classes that can be missed without dropping below target percentage."""
        if self.current_percentage < self.target_percentage:
            return 0
        target = self.target_percentage
        # attended / (total + y) >= target / 100
        numerator = (100.0 * self.classes_attended) - (target * self.total_classes)
        return max(0, math.floor(numerator / target))

    @property
    def status_level(self) -> str:
        pct = self.current_percentage
        if pct >= 80.0:
            return "safe"
        elif pct >= 75.0:
            return "warning"
        return "critical"

    def __str__(self):
        return f"{self.subject_code} - {self.current_percentage}%"
