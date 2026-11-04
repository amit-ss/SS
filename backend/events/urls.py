from django.urls import path
from .views import EventListView, EventDetailView, ToggleSaveEventView, SavedEventsListView

urlpatterns = [
    path('', EventListView.as_view(), name='events-list'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('<int:pk>/save/', ToggleSaveEventView.as_view(), name='event-save-toggle'),
    path('saved/', SavedEventsListView.as_view(), name='events-saved'),
]
