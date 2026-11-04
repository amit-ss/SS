from rest_framework import serializers
from .models import CampusEvent, SavedEvent

class CampusEventSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = CampusEvent
        fields = [
            'id', 'title', 'category', 'category_display', 'description',
            'image_url', 'venue', 'organizer', 'start_date', 'end_date',
            'registration_url', 'is_featured', 'is_saved', 'created_at'
        ]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedEvent.objects.filter(user=request.user, event=obj).exists()
        return False

class SavedEventSerializer(serializers.ModelSerializer):
    event = CampusEventSerializer(read_only=True)

    class Meta:
        model = SavedEvent
        fields = ['id', 'event', 'saved_at']
