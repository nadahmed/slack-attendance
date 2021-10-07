from django.urls import path
from attendance.views.views import TimesheetHandler, SlackUserCreation
from attendance.views.api import PunchIn, PunchOut, ListTimesheets, TimesheetStatus, Statistics

urlpatterns = [
    path('slack/integration/', SlackUserCreation.as_view(), name="slack-integration"),
    path("slack/", TimesheetHandler.as_view(), name="timesheet"),
    path("punchin/", PunchIn.as_view(), name='punchin'),
    path("punchout/", PunchOut.as_view(), name='punchout'),
    path("timesheets/", ListTimesheets.as_view(), name='timesheet_list'),
    path("timesheetstatus/", TimesheetStatus.as_view(), name='timesheet_status'),
    path("statistics/", Statistics.as_view(), name="statistics")
]
