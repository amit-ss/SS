from rest_framework import serializers
from .models import CampusLocation

class CampusLocationSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = CampusLocation
        fields = [
            'id', 'name', 'category', 'category_display', 'block_number',
            'floor_or_room', 'latitude', 'longitude', 'description',
            'qr_code_id', 'image_url', 'is_popular'
        ]
