from rest_framework.serializers import ModelSerializer
from holiday.models import Holiday

class HolidaySerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'