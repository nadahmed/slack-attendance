from rest_framework import viewsets
from holiday.models import Holiday
from holiday.serializers import HolidaySerializer
import django_filters

class HolidayFilter(django_filters.FilterSet):
    # month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Holiday
        fields = [
            # 'month',
            'year'
            ]

class HolidayViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = HolidaySerializer
    queryset = Holiday.objects.all()
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = HolidayFilter
