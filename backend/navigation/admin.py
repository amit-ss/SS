from django.contrib import admin
from .models import CampusLocation

@admin.register(CampusLocation)
class CampusLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'block_number', 'floor_or_room', 'qr_code_id', 'is_popular')
    list_filter = ('category', 'is_popular')
    search_fields = ('name', 'block_number', 'description', 'qr_code_id')
