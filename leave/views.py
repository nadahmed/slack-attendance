from rest_framework import viewsets
from leave.serializers import LeaveTypeSerializer
from leave.models import LeaveType

class LeaveTypeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer