from attendance.models import Timesheet, CheckIn, CheckOut, Shift
from rest_framework.serializers import ModelSerializer


class ShiftSerializer(ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'

class CheckInSerializer(ModelSerializer):
    class Meta:
        model= CheckIn
        fields = '__all__'


class CheckOutSerializer(ModelSerializer):
    class Meta:
        model= CheckOut
        fields = '__all__'

class TimesheetSerializer(ModelSerializer):
    check_in = CheckInSerializer(many=True)
    check_out = CheckOutSerializer(many=True)

    class Meta:
        model = Timesheet
        exclude = ('user',)