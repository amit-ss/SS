from rest_framework import serializers
from .models import SubjectAttendance

class SubjectAttendanceSerializer(serializers.ModelSerializer):
    current_percentage = serializers.ReadOnlyField()
    classes_needed = serializers.ReadOnlyField()
    max_missable_classes = serializers.ReadOnlyField()
    status_level = serializers.ReadOnlyField()

    class Meta:
        model = SubjectAttendance
        fields = [
            'id', 'subject_name', 'subject_code', 'total_classes',
            'classes_attended', 'target_percentage', 'faculty_name',
            'current_percentage', 'classes_needed', 'max_missable_classes',
            'status_level', 'last_updated'
        ]
