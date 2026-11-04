from django.contrib import admin
from .models import CareerProfile, InterviewQuestion

@admin.register(CareerProfile)
class CareerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'resume_score', 'updated_at')
    search_fields = ('user__username', 'target_role')

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'question_type', 'difficulty', 'role_category')
    list_filter = ('question_type', 'difficulty')
    search_fields = ('question', 'sample_answer')
