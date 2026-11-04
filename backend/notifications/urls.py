from django.urls import path
from .views import (
    NotificationListView, MarkNotificationReadView,
    StudyPartnerView, MyCampusDayDashboardView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/mark-read/', MarkNotificationReadView.as_view(), name='notification-mark-read'),
    path('study-partners/', StudyPartnerView.as_view(), name='study-partners'),
    path('dashboard/my-day/', MyCampusDayDashboardView.as_view(), name='my-campus-day'),
]
