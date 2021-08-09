from django.shortcuts import HttpResponse
from django.views import View
from .forms import SlackPayloadForm
from .models import CheckIn, CheckOut, Timesheet
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def check_in_is_valid():
    
    return True

class Payload(View):

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        f = SlackPayloadForm(request.POST)
        if f.is_valid():
            payload = f.save()
            try:
                self._save_to_timesheet(payload)
            except Exception as e:
                if str(e) == "checkin_failed":
                    return HttpResponse("Timesheet not saved. You need to check out first to check in.")
                elif str(e) == "checkout_failed":
                    return HttpResponse("Timesheet not saved. You need to check in first to check out.")
                else:
                    HttpResponse("Opps! Something bad happened. Timesheet was not saved! Please contact admin now!")
        return HttpResponse("Your time has been recorded!")

    def get_timesheet_for_today(self, name):
        try:
            timesheet = Timesheet.objects.filter(Q(name=name)).latest('date')
            if timesheet.date == timezone.now().today().date():
                return timesheet
        except Timesheet.DoesNotExist:
            pass
        return Timesheet.objects.create(name=self.name)


    def _save_to_timesheet(self, SlackPayload):
        timesheet = self.get_timesheet_for_today(name = SlackPayload.user_name)
        if SlackPayload.command == '/in':
            if timesheet.can_check_in():
                CheckIn.objects.create(timesheet=timesheet)
            else:
                raise Exception("checkin_failed")
        elif SlackPayload.command == '/out':
            if timesheet.can_check_out():
                CheckOut.objects.create(timesheet=timesheet)
            else:
                raise Exception("checkout_failed")