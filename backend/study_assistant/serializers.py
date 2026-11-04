from rest_framework import serializers
from .models import StudyDocument, Flashcard, QuizQuestion

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flashcard
        fields = '__all__'

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'

class StudyDocumentSerializer(serializers.ModelSerializer):
    flashcards_count = serializers.IntegerField(source='flashcards.count', read_only=True)
    quizzes_count = serializers.IntegerField(source='quizzes.count', read_only=True)

    class Meta:
        model = StudyDocument
        fields = [
            'id', 'title', 'subject', 'file', 'extracted_text',
            'summary', 'page_count', 'flashcards_count', 'quizzes_count', 'created_at'
        ]
