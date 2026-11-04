from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from django.db.models import Q
from .models import CampusEvent, SavedEvent
from .serializers import CampusEventSerializer, SavedEventSerializer

class EventListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CampusEventSerializer

    def get_queryset(self):
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('q')
        featured = self.request.query_params.get('featured')

        qs = CampusEvent.objects.all()
        if category and category != 'all':
            qs = qs.filter(category=category)
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(venue__icontains=search) |
                Q(organizer__icontains=search)
            )
        if featured:
            qs = qs.filter(is_featured=True)
        return qs.order_by('start_date')

class EventDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CampusEvent.objects.all()
    serializer_class = CampusEventSerializer

class ToggleSaveEventView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        event = CampusEvent.objects.filter(id=pk).first()
        if not event:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response({'is_saved': True, 'message': 'Event bookmarked locally'})

        saved = SavedEvent.objects.filter(user=request.user, event=event).first()
        if saved:
            saved.delete()
            return Response({'is_saved': False, 'message': 'Event removed from saved'})
        else:
            SavedEvent.objects.create(user=request.user, event=event)
            return Response({'is_saved': True, 'message': 'Event saved to calendar'})

class SavedEventsListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            # Return empty or sample
            return Response([])
        saved = SavedEvent.objects.filter(user=request.user).select_related('event')
        return Response(SavedEventSerializer(saved, many=True).data)
