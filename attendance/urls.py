from django.urls import path
from .views import TimesheetHandler, SlackUserCreation


urlpatterns = [
    path('slack/integration/', SlackUserCreation.as_view(), name="slack-integration"),
    path("slack/", TimesheetHandler.as_view(), name="timesheet"),
]
