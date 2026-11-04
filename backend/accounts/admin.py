from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reg_number', 'course', 'branch', 'semester', 'section')
    search_fields = ('user__username', 'reg_number', 'user__email', 'course')
    list_filter = ('course', 'branch', 'semester')
