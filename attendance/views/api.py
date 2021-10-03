from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable
from rest_framework import  permissions
from attendance.models import Timesheet, CheckIn, CheckOut
from django.utils import timezone
from django.db.models import Q
from attendance.exceptions import CheckInvalidException
import json
from django.http.response import JsonResponse


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
            return JsonResponse(data={}, status=200)
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
            return JsonResponse(data={}, status=200)
        else:
            raise NotAcceptable()