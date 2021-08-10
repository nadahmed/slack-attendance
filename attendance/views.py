from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.views import View
from .forms import SlackPayloadForm
from .models import CheckIn, CheckOut, Timesheet
from django.utils import timezone
from django.db.models import Q
import requests
from django.conf import settings
# Create your views here.




class CheckInvalidException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

@method_decorator(csrf_exempt, name='dispatch')
class Payload(View):

    def send_msg_to_slack(self, url, channel_id, msg):
        headers = {'Authorization': 'Bearer %s' % settings.SLACK_OAUTH_TOKEN}
        return requests.post(
            settings.SLACK_WEBHOOKS_URL,
            headers=headers,
            json={
                "channel": channel_id,
                "text": msg
            })

    def get(self, request):
        return HttpResponse("OK")

    def post(self, request):
        f = SlackPayloadForm(request.POST)
        if f.is_valid():
            payload = f.save()
            try:
                timesheet = self._save_to_timesheet(payload)
                if (timesheet.is_checked_out()):
                    self.send_msg_to_slack(payload.response_url, payload.channel_id, '@%s has checked out!' % payload.user_name)
                    return HttpResponse("Your have checked out! Your total work hour is %s." % timesheet.total_work_hour())
                else:
                    self.send_msg_to_slack(payload.response_url, payload.channel_id, '@%s has checked in!' % payload.user_name)
                    return HttpResponse(
                    "Welcome back! You have checked in! Your total work hour is %s and counting!" % timesheet.total_work_hour()
                    )

            except CheckInvalidException as e:
                if str(e) == "checkin_failed":
                    return HttpResponse("Timesheet not saved. You need to check out first to check in.")
                elif str(e) == "checkout_failed":
                    return HttpResponse("Timesheet not saved. You need to check in first to check out.")
                else:
                    HttpResponse("Opps! Something bad happened. Timesheet was not saved! Please contact admin now!")
        return HttpResponse("Oops! Something went wrong! Please notify the admins now!")

    def get_timesheet_for_today(self, name):
        try:
            timesheet = Timesheet.objects.filter(Q(name=name)).latest('date')
            if timesheet.date == timezone.now().today().date():
                return timesheet
        except Timesheet.DoesNotExist:
            pass
        return Timesheet.objects.create(name=name)


    def _save_to_timesheet(self, SlackPayload):
        timesheet = self.get_timesheet_for_today(name = SlackPayload.user_name)
        text = SlackPayload.text
        if SlackPayload.command == '/in':
            if timesheet.can_check_in():
                CheckIn.objects.create(timesheet=timesheet, message=text)
            else:
                raise CheckInvalidException("checkin_failed")
        elif SlackPayload.command == '/out':
            if timesheet.can_check_out():
                CheckOut.objects.create(timesheet=timesheet,  message=text)
            else:
                raise CheckInvalidException("checkout_failed")
        return timesheet