from django.urls import path
from .views import (
    AttendanceSummaryView, SubjectAttendanceListCreateView,
    SubjectAttendanceDetailView, AttendancePredictorView
)

urlpatterns = [
    path('summary/', AttendanceSummaryView.as_view(), name='attendance-summary'),
    path('subjects/', SubjectAttendanceListCreateView.as_view(), name='attendance-subjects'),
    path('subjects/<int:pk>/', SubjectAttendanceDetailView.as_view(), name='attendance-subject-detail'),
    path('predict/', AttendancePredictorView.as_view(), name='attendance-predict'),
]
