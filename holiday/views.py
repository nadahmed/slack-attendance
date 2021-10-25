from rest_framework import viewsets, status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        data = request.data.get('items', request.data)
        many = isinstance(data, list)
        print (data, many)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
        )
