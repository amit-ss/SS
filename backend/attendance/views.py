import math
from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from .models import SubjectAttendance
from .serializers import SubjectAttendanceSerializer

class AttendanceSummaryView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        records = SubjectAttendance.objects.all()
        total_held = sum(r.total_classes for r in records)
        total_attended = sum(r.classes_attended for r in records)
        overall_pct = round((total_attended / total_held * 100), 1) if total_held > 0 else 100.0

        critical_count = sum(1 for r in records if r.current_percentage < 75.0)
        warning_count = sum(1 for r in records if 75.0 <= r.current_percentage < 80.0)

        return Response({
            'overall_percentage': overall_pct,
            'total_subjects': records.count(),
            'total_classes_held': total_held,
            'total_classes_attended': total_attended,
            'critical_subjects_count': critical_count,
            'warning_subjects_count': warning_count,
            'records': SubjectAttendanceSerializer(records, many=True).data
        })

class SubjectAttendanceListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = SubjectAttendance.objects.all()
    serializer_class = SubjectAttendanceSerializer

class SubjectAttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = SubjectAttendance.objects.all()
    serializer_class = SubjectAttendanceSerializer

class AttendancePredictorView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Calculates custom prediction scenarios:
        Input: total_classes, classes_attended, target_percentage (e.g. 75, 80, 85)
        """
        try:
            total = int(request.data.get('total_classes', 0))
            attended = int(request.data.get('classes_attended', 0))
            target = float(request.data.get('target_percentage', 75.0))

            if total <= 0 or attended < 0 or attended > total:
                return Response({'error': 'Invalid class counts provided'}, status=status.HTTP_400_BAD_REQUEST)

            current_pct = round((attended / total) * 100.0, 1)

            if current_pct >= target:
                # Can miss classes
                numerator = (100.0 * attended) - (target * total)
                max_missable = max(0, math.floor(numerator / target))
                needed = 0
                message = f"You are safe! You can miss up to {max_missable} upcoming classes while maintaining >= {target}%."
            else:
                # Must attend
                numerator = (target * total) - (100.0 * attended)
                denominator = 100.0 - target
                needed = max(0, math.ceil(numerator / denominator)) if denominator > 0 else 0
                max_missable = 0
                message = f"Warning: You need to attend the next {needed} consecutive classes to reach {target}%."

            return Response({
                'current_percentage': current_pct,
                'target_percentage': target,
                'classes_needed_for_target': needed,
                'max_classes_can_miss': max_missable,
                'is_eligible_for_exams': current_pct >= 75.0,
                'message': message
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
