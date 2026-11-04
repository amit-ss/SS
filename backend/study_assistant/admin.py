from django.contrib import admin
from .models import StudyDocument, Flashcard, QuizQuestion

@admin.register(StudyDocument)
class StudyDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'page_count', 'created_at')
    search_fields = ('title', 'subject', 'extracted_text')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('front', 'is_mastered', 'created_at')
    list_filter = ('is_mastered',)

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'correct_index')
