from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import LostFoundItem, ItemClaim
from .serializers import LostFoundItemSerializer, ItemClaimSerializer

class ItemListCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        item_type = request.query_params.get('type')
        category = request.query_params.get('category')
        search = request.query_params.get('q')

        qs = LostFoundItem.objects.filter(is_moderated=True)
        if item_type and item_type != 'all':
            qs = qs.filter(item_type=item_type)
        if category and category != 'all':
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location_name__icontains=search)
            )

        return Response(LostFoundItemSerializer(qs, many=True).data)

    def post(self, request):
        serializer = LostFoundItemSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            instance = serializer.save(user=user)
            return Response(LostFoundItemSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = LostFoundItem.objects.all()
    serializer_class = LostFoundItemSerializer

class SubmitClaimView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        item = LostFoundItem.objects.filter(id=pk).first()
        if not item:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        claimant_name = request.data.get('claimant_name', '').strip()
        claimant_phone = request.data.get('claimant_phone', '').strip()
        proof_desc = request.data.get('proof_description', '').strip()

        if not claimant_name or not claimant_phone or not proof_desc:
            return Response({'error': 'Name, phone number, and proof description are required'}, status=status.HTTP_400_BAD_REQUEST)

        claim = ItemClaim.objects.create(
            item=item,
            claimant=request.user if request.user.is_authenticated else None,
            claimant_name=claimant_name,
            claimant_phone=claimant_phone,
            proof_description=proof_desc
        )
        return Response({
            'claim': ItemClaimSerializer(claim).data,
            'message': 'Your ownership claim has been submitted to the reporter/admin for review.'
        }, status=status.HTTP_201_CREATED)
