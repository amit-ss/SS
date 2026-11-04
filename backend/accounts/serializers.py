from rest_framework import serializers
from django.contrib.auth.models import User
from .models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'reg_number', 'course', 'branch', 'semester', 'section',
            'phone', 'profile_photo', 'dark_mode', 'notifications_enabled',
            'career_goal', 'created_at', 'updated_at'
        ]

class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'student_profile']

class RegisterSerializer(serializers.ModelSerializer):
    reg_number = serializers.CharField(write_only=True)
    course = serializers.CharField(write_only=True, required=False, default="B.Tech Computer Science & Engineering")
    branch = serializers.CharField(write_only=True, required=False, default="CSE")
    semester = serializers.IntegerField(write_only=True, required=False, default=5)
    section = serializers.CharField(write_only=True, required=False, default="K22DF")
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'reg_number', 'course', 'branch', 'semester', 'section']

    def create(self, validated_data):
        reg_number = validated_data.pop('reg_number')
        course = validated_data.pop('course', "B.Tech Computer Science & Engineering")
        branch = validated_data.pop('branch', "CSE")
        semester = validated_data.pop('semester', 5)
        section = validated_data.pop('section', "K22DF")
        password = validated_data.pop('password')

        user = User.objects.create_user(password=password, **validated_data)
        StudentProfile.objects.create(
            user=user,
            reg_number=reg_number,
            course=course,
            branch=branch,
            semester=semester,
            section=section
        )
        return user
