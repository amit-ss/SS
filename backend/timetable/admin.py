from django.contrib import admin
from .models import Faculty, Course, ClassTimetable, ExamSchedule

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'email', 'phone', 'office_room')
    search_fields = ('name', 'department', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'assigned_faculty', 'credits')
    search_fields = ('code', 'name')

@admin.register(ClassTimetable)
class ClassTimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_of_week', 'start_time', 'end_time', 'room_number', 'section')
    list_filter = ('day_of_week', 'section')

@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_date', 'start_time', 'end_time', 'room_number', 'exam_type')
    list_filter = ('exam_type', 'exam_date')
