from django.urls import path
from .views import LocationListView, LocationDetailView, QRScannerLookupView

urlpatterns = [
    path('locations/', LocationListView.as_view(), name='navigation-locations'),
    path('locations/<int:pk>/', LocationDetailView.as_view(), name='navigation-location-detail'),
    path('qr/<str:qr_code_id>/', QRScannerLookupView.as_view(), name='navigation-qr-lookup'),
]
