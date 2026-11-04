from datetime import datetime, time
from itertools import groupby
from django.utils import timezone
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import Faculty, Course, ClassTimetable, ExamSchedule
from .serializers import FacultySerializer, CourseSerializer, ClassTimetableSerializer, ExamScheduleSerializer

DAY_MAP = {
    0: 'MON',
    1: 'TUE',
    2: 'WED',
    3: 'THU',
    4: 'FRI',
    5: 'SAT',
    6: 'SUN'
}

def check_time_conflict(day: str, start: time, end: time, exclude_id=None):
    """Detects timetable conflicts on the same day."""
    qs = ClassTimetable.objects.filter(day_of_week=day)
    if exclude_id:
        qs = qs.exclude(id=exclude_id)
    
    conflicts = []
    for entry in qs:
        # Overlap: max(start1, start2) < min(end1, end2)
        if max(start, entry.start_time) < min(end, entry.end_time):
            conflicts.append(f"Conflicts with {entry.course.code} ({entry.start_time}-{entry.end_time} in {entry.room_number})")
    return conflicts

class WeeklyTimetableView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        timetable = ClassTimetable.objects.select_related('course', 'course__assigned_faculty').all()
        grouped = {}
        for code, label in ClassTimetable.DAY_CHOICES:
            grouped[code] = {
                'day_code': code,
                'day_name': label,
                'classes': []
            }

        for item in timetable:
            if item.day_of_week in grouped:
                grouped[item.day_of_week]['classes'].append(ClassTimetableSerializer(item).data)

        return Response(list(grouped.values()))

class TodayTimetableView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.localtime()
        day_code = DAY_MAP.get(now.weekday(), 'MON')
        classes = ClassTimetable.objects.filter(day_of_week=day_code).select_related('course', 'course__assigned_faculty')
        return Response({
            'today': day_code,
            'classes': ClassTimetableSerializer(classes, many=True).data
        })

class NextClassView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        now = timezone.localtime()
        current_time = now.time()
        day_code = DAY_MAP.get(now.weekday(), 'MON')

        # Find classes today starting after current_time
        upcoming = ClassTimetable.objects.filter(
            day_of_week=day_code,
            end_time__gte=current_time
        ).select_related('course', 'course__assigned_faculty').order_by('start_time').first()

        if not upcoming:
            # Look at first class tomorrow
            next_day_idx = (now.weekday() + 1) % 7
            next_day_code = DAY_MAP.get(next_day_idx, 'MON')
            upcoming = ClassTimetable.objects.filter(
                day_of_week=next_day_code
            ).select_related('course', 'course__assigned_faculty').order_by('start_time').first()

        if upcoming:
            return Response({
                'has_class': True,
                'next_class': ClassTimetableSerializer(upcoming).data
            })
        return Response({'has_class': False, 'message': 'No more classes scheduled.'})

class ClassListCreateView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        classes = ClassTimetable.objects.select_related('course', 'course__assigned_faculty').all()
        return Response(ClassTimetableSerializer(classes, many=True).data)

    def post(self, request):
        serializer = ClassTimetableSerializer(data=request.data)
        if serializer.is_valid():
            day = serializer.validated_data['day_of_week']
            start = serializer.validated_data['start_time']
            end = serializer.validated_data['end_time']
            
            conflicts = check_time_conflict(day, start, end)
            instance = serializer.save()
            return Response({
                'data': ClassTimetableSerializer(instance).data,
                'conflicts': conflicts,
                'message': 'Class added successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ClassTimetable.objects.all()
    serializer_class = ClassTimetableSerializer

class CourseListView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class FacultyListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer

class ExamScheduleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ExamSchedule.objects.select_related('course').all()
    serializer_class = ExamScheduleSerializer
