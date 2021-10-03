from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable
from rest_framework import  permissions
from attendance.models import Timesheet, CheckIn, CheckOut
from django.utils import timezone
from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from attendance.serializers import TimesheetSerializer
from django.conf import settings
import requests

def get_timesheet_for_today(user):
    try:
        timesheet = Timesheet.objects.filter(Q(user=user)).latest('date')
        if timesheet.date == timezone.localtime(timezone.now()).today().date():
            return timesheet
    except Timesheet.DoesNotExist:
        pass
    return Timesheet.objects.create(name="http", user=user)


class PunchIn(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_timesheet_for_today(self, user):
        try:
            timesheet = Timesheet.objects.filter(Q(user=user)).latest('date')
            if timesheet.date == timezone.localtime(timezone.now()).today().date():
                return timesheet
        except Timesheet.DoesNotExist:
            pass
        return Timesheet.objects.create(name="http", user=user)

    def post(self, request):
        sheet = get_timesheet_for_today(request.user)
 
        if sheet.can_check_in():
            checkin = CheckIn.objects.create(timesheet=sheet)
            return JsonResponse(data={"time": checkin.time, "day": sheet.date}, status=200)
        else:
            raise NotAcceptable()

class PunchOut(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request):
        sheet = get_timesheet_for_today(request.user)
 
        if sheet.can_check_out():
            checkout = CheckOut.objects.create(timesheet=sheet)
            return JsonResponse(data={"time": checkout.time, "day": sheet.date}, status=200)
        else:
            raise NotAcceptable()

class ListTimesheets(viewsets.ViewSet):
    def list(self, request):
        queryset = Timesheet.objects.filter(user=request.user)
        serializer = TimesheetSerializer(queryset, many=True)
        return Response(serializer.data)

class TimesheetStatus(APIView):
    def get(self, request):
        sheet = get_timesheet_for_today(request.user)

        data = {
            "first_punch_in": sheet.check_in.all().earliest('time').time,
            "last_activity": {"activity":'punch_out', "time": sheet.check_out.all().latest('time').time} if sheet.is_checked_out() else {"activity":'punch_in', "time": sheet.check_in.all().latest('time').time}
        }

        return JsonResponse(data=data, status=200)