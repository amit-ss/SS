from datetime import datetime
from django.utils import timezone
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import Notification, StudyPartnerRequest
from .serializers import NotificationSerializer, StudyPartnerRequestSerializer
from timetable.models import ClassTimetable
from timetable.serializers import ClassTimetableSerializer
from attendance.models import SubjectAttendance
from events.models import CampusEvent
from events.serializers import CampusEventSerializer

DAY_MAP = {0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'}

class NotificationListView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        qs = Notification.objects.all().order_by('-created_at')[:25]
        return Response(NotificationSerializer(qs, many=True).data)

class MarkNotificationReadView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, pk):
        notif = Notification.objects.filter(id=pk).first()
        if notif:
            notif.is_read = True
            notif.save()
            return Response({'message': 'Marked as read'})
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

class StudyPartnerView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        # Sample active study partners in LPU
        partners = [
            {
                "id": 1,
                "name": "Rohan Verma",
                "branch": "B.Tech CSE - 6th Sem",
                "focus_area": "Data Structures & Algorithms (LeetCode 300+)",
                "subjects": ["DSA", "Operating Systems", "Competitive Coding"],
                "looking_for": "Mock interview partner for Microsoft placement drive.",
                "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150"
            },
            {
                "id": 2,
                "name": "Ananya Sharma",
                "branch": "B.Tech CSE (AI & ML) - 5th Sem",
                "focus_area": "Machine Learning & Deep Learning",
                "subjects": ["NLP", "PyTorch", "Computer Vision"],
                "looking_for": "Teammate for upcoming LPU Smart India Hackathon.",
                "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
            },
            {
                "id": 3,
                "name": "Sahil Preet Singh",
                "branch": "B.Tech IT - 5th Sem",
                "focus_area": "Full Stack Web & Cloud Architecture",
                "subjects": ["React Native", "Django", "AWS Cloud"],
                "looking_for": "Collaborator to build campus open-source projects.",
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
            }
        ]
        return Response(partners)

    def post(self, request):
        target_name = request.data.get('partner_name', 'Student')
        subject = request.data.get('subject', 'General Study')
        message = request.data.get('message', 'Hi! Would love to study together.')

        return Response({
            'status': 'sent',
            'message': f"Connection request successfully sent to {target_name} for '{subject}'!"
        })

class MyCampusDayDashboardView(views.APIView):
    """
    Consolidated intelligent payload for the mobile Home Dashboard:
    - Greeting with student name
    - Current date & formatted time
    - Next upcoming class
    - Today's timetable
    - Attendance summary
    - Upcoming events
    - Unread notification count
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.localtime()
        current_time = now.time()
        day_code = DAY_MAP.get(now.weekday(), 'MON')

        # Today's classes
        today_classes = ClassTimetable.objects.filter(day_of_week=day_code).select_related('course', 'course__assigned_faculty').order_by('start_time')

        # Next upcoming class
        next_class = today_classes.filter(end_time__gte=current_time).first()
        if not next_class:
            # Check tomorrow
            next_day_code = DAY_MAP.get((now.weekday() + 1) % 7, 'MON')
            next_class = ClassTimetable.objects.filter(day_of_week=next_day_code).select_related('course', 'course__assigned_faculty').order_by('start_time').first()

        # Attendance
        records = SubjectAttendance.objects.all()
        total_held = sum(r.total_classes for r in records)
        total_attended = sum(r.classes_attended for r in records)
        overall_pct = round((total_attended / total_held * 100), 1) if total_held > 0 else 81.5

        # Upcoming events (next 3)
        upcoming_events = CampusEvent.objects.all().order_by('start_date')[:4]

        # Recent notifications
        recent_notifs = Notification.objects.all().order_by('-created_at')[:3]
        unread_count = Notification.objects.filter(is_read=False).count()

        student_name = "Amit Singh"
        reg_number = "12204567"
        if request.user.is_authenticated:
            student_name = request.user.get_full_name() or request.user.username
            if hasattr(request.user, 'student_profile'):
                reg_number = request.user.student_profile.reg_number

        return Response({
            'student_name': student_name,
            'reg_number': reg_number,
            'date_formatted': now.strftime("%A, %d %B %Y"),
            'next_class': ClassTimetableSerializer(next_class).data if next_class else None,
            'today_classes_count': today_classes.count(),
            'today_classes': ClassTimetableSerializer(today_classes, many=True).data,
            'attendance': {
                'overall_percentage': overall_pct,
                'status': 'safe' if overall_pct >= 75.0 else 'critical',
                'target': 75.0,
                'total_subjects': records.count() or 5
            },
            'upcoming_events': CampusEventSerializer(upcoming_events, many=True, context={'request': request}).data,
            'unread_notifications_count': unread_count,
            'recent_notifications': NotificationSerializer(recent_notifs, many=True).data,
            'quick_actions': [
                {"id": "ask_ai", "title": "Ask CampusGPT", "icon": "sparkles", "route": "AIChat"},
                {"id": "timetable", "title": "Smart Timetable", "icon": "calendar", "route": "Timetable"},
                {"id": "attendance", "title": "Attendance Predictor", "icon": "calculator", "route": "Attendance"},
                {"id": "map", "title": "Campus Navigation", "icon": "map", "route": "Campus"},
                {"id": "study", "title": "Study Assistant", "icon": "book-open", "route": "StudyAssistant"},
                {"id": "lost_found", "title": "Lost & Found", "icon": "search", "route": "LostFound"},
                {"id": "events", "title": "Event Finder", "icon": "star", "route": "Events"},
                {"id": "career", "title": "Career Assistant", "icon": "briefcase", "route": "Career"}
            ]
        })
