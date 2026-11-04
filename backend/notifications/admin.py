from django.contrib import admin
from .models import Notification, StudyPartnerRequest

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')

@admin.register(StudyPartnerRequest)
class StudyPartnerRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject_or_goal', 'status', 'created_at')
    list_filter = ('status',)
