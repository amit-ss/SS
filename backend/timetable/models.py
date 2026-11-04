from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    office_room = models.CharField(max_length=50, default="Block 34-402")

    def __str__(self):
        return f"{self.name} ({self.department})"

class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)
    assigned_faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    credits = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ClassTimetable(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='timetable_entries')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50, help_text="e.g. 27-407, 34-602")
    section = models.CharField(max_length=20, default="K22DF")

    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name_plural = "Class Timetables"

    def __str__(self):
        return f"{self.course.code} [{self.day_of_week}] {self.start_time}-{self.end_time} ({self.room_number})"

class ExamSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=50)
    exam_type = models.CharField(max_length=50, default="Mid-Term (CA)")

    class Meta:
        ordering = ['exam_date', 'start_time']

    def __str__(self):
        return f"{self.course.code} Exam on {self.exam_date} ({self.room_number})"
