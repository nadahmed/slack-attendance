from django.db.models import fields
from rest_framework import serializers
from leave.models import LeaveType, LeaveForm, Approval



class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'

class LeaveFormCreationSerializer(serializers.ModelSerializer):
    
    # leave_type = serializers.PrimaryKeyRelatedField(read_only=True)
    # date_from = serializers.DateField(format="%Y-%m-%d")
    # date_to = serializers.DateField(format="%Y-%m-%d")
    class Meta:
        model = LeaveForm
        exclude = ('approval',)

class LeaveFormSerializer(serializers.ModelSerializer):
    approval = ApprovalSerializer()
    leave_type = LeaveTypeSerializer()

    class Meta:
        model = LeaveForm
        # fields = '__all__'
        exclude = ('applicant', )