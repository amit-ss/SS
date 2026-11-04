from django.contrib import admin
from .models import CampusEvent, SavedEvent

@admin.register(CampusEvent)
class CampusEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'venue', 'start_date', 'organizer', 'is_featured')
    list_filter = ('category', 'is_featured', 'start_date')
    search_fields = ('title', 'description', 'venue', 'organizer')

@admin.register(SavedEvent)
class SavedEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'saved_at')
