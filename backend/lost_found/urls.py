from django.urls import path
from .views import ItemListCreateView, ItemDetailView, SubmitClaimView

urlpatterns = [
    path('items/', ItemListCreateView.as_view(), name='lost-found-items'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='lost-found-item-detail'),
    path('items/<int:pk>/claim/', SubmitClaimView.as_view(), name='lost-found-submit-claim'),
]
