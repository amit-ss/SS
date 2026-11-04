from rest_framework import serializers
from .models import Faculty, Course, ClassTimetable, ExamSchedule

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    assigned_faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source='assigned_faculty', write_only=True, required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'credits', 'assigned_faculty', 'faculty_id']

class ClassTimetableSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = ClassTimetable
        fields = [
            'id', 'course', 'course_id', 'day_of_week', 'day_display',
            'start_time', 'end_time', 'room_number', 'section'
        ]

class ExamScheduleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = ExamSchedule
        fields = '__all__'
