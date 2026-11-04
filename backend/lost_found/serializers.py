from rest_framework import serializers
from .models import LostFoundItem, ItemClaim

class ItemClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemClaim
        fields = '__all__'

class LostFoundItemSerializer(serializers.ModelSerializer):
    claims = ItemClaimSerializer(many=True, read_only=True)
    item_type_display = serializers.CharField(source='get_item_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = LostFoundItem
        fields = [
            'id', 'user', 'reporter_name', 'item_type', 'item_type_display',
            'title', 'category', 'category_display', 'description', 'location_name',
            'date_time', 'photo', 'photo_url', 'contact_phone', 'status', 'claims'
        ]
