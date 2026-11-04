from django.contrib import admin
from .models import ChatMessage, KnowledgeDocument

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'session_id', 'timestamp', 'content_preview')
    list_filter = ('role', 'timestamp')
    search_fields = ('content', 'session_id')

    def content_preview(self, obj):
        return obj.content[:50]

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'source_reference', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'content', 'source_reference')
