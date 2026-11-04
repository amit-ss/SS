from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'online',
        'application': 'CampusGPT – Your Smart LPU Campus Companion API',
        'version': '1.0.0',
        'university': 'Lovely Professional University (LPU)',
        'endpoints': {
            'auth': '/api/v1/auth/',
            'chatbot': '/api/v1/chatbot/',
            'timetable': '/api/v1/timetable/',
            'attendance': '/api/v1/attendance/',
            'navigation': '/api/v1/navigation/',
            'study_assistant': '/api/v1/study/',
            'lost_found': '/api/v1/lost-found/',
            'events': '/api/v1/events/',
            'career': '/api/v1/career/',
            'notifications': '/api/v1/notifications/',
            'dashboard': '/api/v1/dashboard/my-day/',
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', health_check, name='health-check'),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/chatbot/', include('chatbot.urls')),
    path('api/v1/timetable/', include('timetable.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/navigation/', include('navigation.urls')),
    path('api/v1/study/', include('study_assistant.urls')),
    path('api/v1/lost-found/', include('lost_found.urls')),
    path('api/v1/events/', include('events.urls')),
    path('api/v1/career/', include('career.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
