from django.urls import path
from .views import (
    WeeklyTimetableView, TodayTimetableView, NextClassView,
    ClassListCreateView, ClassDetailView, CourseListView,
    FacultyListView, ExamScheduleListView
)

urlpatterns = [
    path('weekly/', WeeklyTimetableView.as_view(), name='timetable-weekly'),
    path('today/', TodayTimetableView.as_view(), name='timetable-today'),
    path('next-class/', NextClassView.as_view(), name='timetable-next-class'),
    path('classes/', ClassListCreateView.as_view(), name='timetable-classes'),
    path('classes/<int:pk>/', ClassDetailView.as_view(), name='timetable-class-detail'),
    path('courses/', CourseListView.as_view(), name='timetable-courses'),
    path('faculty/', FacultyListView.as_view(), name='timetable-faculty'),
    path('exams/', ExamScheduleListView.as_view(), name='timetable-exams'),
]
