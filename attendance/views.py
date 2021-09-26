from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.views import View
from .forms import SlackPayloadForm
from .models import CheckIn, CheckOut, Timesheet, SlackUser
from django.utils import timezone
from django.db.models import Q
import requests
from django.conf import settings
from re import search
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
# Create your views here.

class SlackUserCreation(APIView):
    
    permission_classes = [
        permissions.IsAuthenticated
        ]

    def post(self, request, format=None):
        if "id" in request.data:
            try:
                SlackUser.objects.create(user=request.user, slack_id= request.data['id'])
                return HttpResponse(status=200)
            except ValidationError:
                return HttpResponseForbidden({"message": "slack already integrated. if you want to re-integrate slack ask the admins."})
        return HttpResponseBadRequest({"message": "something went wrong."})

@method_decorator(csrf_exempt, name='dispatch')
class TimesheetHandler(APIView):
   
    permission_classes=[

    ]
    def send_msg_to_slack(self, url, channel_id, msg):
        headers = {'Authorization': 'Bearer %s' % settings.SLACK_OAUTH_TOKEN}
        return requests.post(
            settings.SLACK_WEBHOOKS_URL,
            headers=headers,
            json={
                "channel": channel_id,
                "text": msg
            })
    def post(self, request):
        f = SlackPayloadForm(request.POST)
        # print(f)
        if f.is_valid():

            payload = f.save(commit=False)
            
            if not search(r'/in|/out', payload.command):
                return HttpResponse("wrong command!")
            
            try: 
                slackuser = SlackUser.objects.get(slack_id=payload.user_id)
                slackuser.slack_user = payload.user_name
                slackuser.response_url = payload.response_url
                slackuser.save()

                try:
                    timesheet = self._save_to_timesheet( slackuser, payload)
                    if (timesheet.is_checked_out()):
                        self.send_msg_to_slack(payload.response_url, payload.channel_id, '@%s has checked out!' % slackuser.user.get_full_name())
                        return HttpResponse("You have checked out! Your total work hour is %s." % timesheet.total_work_hour())
                    else:
                        self.send_msg_to_slack(payload.response_url, payload.channel_id, '@%s has checked in!' % slackuser.user.get_full_name())
                        return HttpResponse(
                        "Welcome back! You have checked in! Your total work hour is %s and counting!" % timesheet.total_work_hour()
                        )

                except CheckInvalidException as e:
                    if str(e) == "checkin_failed":
                        return HttpResponse("Timesheet not saved. You need to check out first to check in.")
                    elif str(e) == "checkout_failed":
                        return HttpResponse("Timesheet not saved. You need to check in first to check out.")
                    else:
                        HttpResponse("Omg! This was impossible to happen. Timesheet was not saved! Please contact admin now!")
            
            except SlackUser.DoesNotExist:
                data = {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hello! Before you can \"{}\" you need to integrate Slack to Hivecore. Please click the button below to do so. Please, comeback and try again once you are done.".format(payload.command)
                            }
                        },
                        {
                            "type": "actions",
                            "elements": [
                                {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Integrate"
                                    },
                                    "style": "primary",
                                    "url": "https://slackintegration.hivecorelimited.com/slack/{}".format(payload.user_id)
                                }
                            ]
                        }
                    ]
                }  
                return JsonResponse(data)
        return HttpResponse("Oops! Something went wrong! Please notify the admins now!")

    
    def get_timesheet_for_today(self, slackuser, name):
        try:
            timesheet = Timesheet.objects.filter(Q(name=name, user=slackuser.user)).latest('date')
            if timesheet.date == timezone.now().today().date():
                return timesheet
        except Timesheet.DoesNotExist:
            pass
        return Timesheet.objects.create(name=name, user=slackuser.user)


    def _save_to_timesheet(self, slackuser, SlackPayload):
        timesheet = self.get_timesheet_for_today(slackuser=slackuser, name = SlackPayload.user_name)
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
        else:
            raise CheckInvalidException("checkout_failed")
        return timesheet

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
                    return HttpResponse("You have checked out! Your total work hour is %s." % timesheet.total_work_hour())
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
                    HttpResponse("Omg! This was impossible to happen. Timesheet was not saved! Please contact admin now!")
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