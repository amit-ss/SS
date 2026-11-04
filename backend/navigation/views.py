from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import CampusLocation
from .serializers import CampusLocationSerializer

class LocationListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CampusLocationSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('q')
        popular = self.request.query_params.get('popular')

        qs = CampusLocation.objects.all()
        if category and category != 'all':
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(
                Q(name__icontains=search) |
                Q(block_number__icontains=search) |
                Q(floor_or_room__icontains=search) |
                Q(description__icontains=search)
            )
        if popular:
            qs = qs.filter(is_popular=True)
        return qs.order_by('name')

class LocationDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CampusLocation.objects.all()
    serializer_class = CampusLocationSerializer

class QRScannerLookupView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, qr_code_id):
        qr_code_id = qr_code_id.strip()
        location = CampusLocation.objects.filter(qr_code_id__iexact=qr_code_id).first()
        if not location:
            # Flexible match for plain block names typed by hand, e.g. "Block 34"
            location = CampusLocation.objects.filter(block_number__iexact=qr_code_id).first()

        if location:
            return Response({
                'found': True,
                'location': CampusLocationSerializer(location).data,
                'message': f"Verified LPU Campus Location: {location.name}"
            })
        return Response({
            'found': False,
            'message': f"No verified LPU location registered with QR ID: '{qr_code_id}'"
        }, status=status.HTTP_404_NOT_FOUND)
