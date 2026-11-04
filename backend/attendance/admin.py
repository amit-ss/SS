from django.contrib import admin
from .models import SubjectAttendance

@admin.register(SubjectAttendance)
class SubjectAttendanceAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'classes_attended', 'total_classes', 'current_percentage', 'status_level')
    list_filter = ('target_percentage',)
    search_fields = ('subject_code', 'subject_name')
