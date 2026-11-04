from django.contrib import admin
from .models import LostFoundItem, ItemClaim

@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'category', 'location_name', 'status', 'is_moderated')
    list_filter = ('item_type', 'category', 'status', 'is_moderated')
    search_fields = ('title', 'description', 'location_name')

@admin.register(ItemClaim)
class ItemClaimAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimant_name', 'claimant_phone', 'status', 'created_at')
    list_filter = ('status',)
