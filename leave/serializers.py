from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer
from leave.models import LeaveType, LeaveForm, Approval

class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveFormSerializer(ModelSerializer):
    class Meta:
        model = LeaveForm
