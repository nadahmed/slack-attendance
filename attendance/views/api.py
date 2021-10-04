from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable
from rest_framework import  permissions
from attendance.models import Timesheet, CheckIn, CheckOut, User
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from attendance.serializers import TimesheetSerializer


class PunchIn(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]


    def post(self, request):
        sheet = Timesheet.get_or_create_for_today(request.user)
 
        if sheet.can_check_in():
            checkin = CheckIn.objects.create(timesheet=sheet)
            return JsonResponse(data={"time": checkin.time, "day": sheet.date}, status=200)
        else:
            raise NotAcceptable(detail="You can only punch in after you punch out.")

class PunchOut(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        sheet = Timesheet.get_or_create_for_today(request.user)
 
        if sheet.can_check_out():
            checkout = CheckOut.objects.create(timesheet=sheet)
            return JsonResponse(data={"time": checkout.time, "day": sheet.date}, status=200)
        else:
            raise NotAcceptable(detail="You can only punch out after you punch in.")

import django_filters

class TimesheetFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')

    class Meta:
        model = Timesheet
        fields = ['month', 'year']

class ListTimesheets(ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = TimesheetSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    # search_fields = []
    filter_class = TimesheetFilter
    def get_queryset(self):
        return Timesheet.objects.filter(user=self.request.user)

    # def list(self, request):
    #     queryset = Timesheet.objects.filter(user=request.user)
    #     serializer = TimesheetSerializer(queryset, many=True)
    #     return Response(serializer.data)

class TimesheetStatus(APIView):
    def get(self, request):
        try:
            sheet = Timesheet.objects.get(user=request.user, date=timezone.localtime(timezone.now()).today().date())
        except Timesheet.DoesNotExist:
            data = {
                "date": "",
                "first_punch_in": "",
                "last_activity": {"activity":"", "time": ""}
            }
            return JsonResponse(data=data, status=200)
        data = {
            "date": sheet.date,
            "first_punch_in": sheet.check_in.all().earliest('time').time,
            "last_activity": {"activity":'punch_out', "time": sheet.check_out.all().latest('time').time} if sheet.is_checked_out() else {"activity":'punch_in', "time": sheet.check_in.all().latest('time').time}
        }

        return JsonResponse(data=data, status=200)