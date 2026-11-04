from django.urls import path
from .views import SendMessageView, ChatHistoryView, ClearHistoryView, SuggestedPromptsView, AIProvidersView

urlpatterns = [
    path('message/', SendMessageView.as_view(), name='chatbot-message'),
    path('history/', ChatHistoryView.as_view(), name='chatbot-history'),
    path('history/clear/', ClearHistoryView.as_view(), name='chatbot-clear-history'),
    path('suggested-prompts/', SuggestedPromptsView.as_view(), name='chatbot-suggested-prompts'),
    path('providers/', AIProvidersView.as_view(), name='chatbot-providers'),
]
