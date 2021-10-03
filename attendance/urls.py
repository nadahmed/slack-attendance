from django.urls import path
from attendance.views.views import TimesheetHandler, SlackUserCreation
from attendance.views.api import PunchIn, PunchOut

urlpatterns = [
    path('slack/integration/', SlackUserCreation.as_view(), name="slack-integration"),
    path("slack/", TimesheetHandler.as_view(), name="timesheet"),
    path("punchin/", PunchIn.as_view(), name='punchin'),
    path("punchout/", PunchOut.as_view(), name='punchout')
]
