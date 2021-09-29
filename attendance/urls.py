from django.urls import path
from .views import Payload, TimesheetHandler, SlackUserCreation


urlpatterns = [
    path('slack/integration/', SlackUserCreation.as_view(), name="slack-integration"),
    path("attendance/slack/", TimesheetHandler.as_view(), name="timesheet"),
]
