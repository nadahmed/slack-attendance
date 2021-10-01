import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def getLocalTime():
    return timezone.localtime(timezone.now())

class SlackUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="slack", unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    slack_id = models.CharField(max_length=50, unique=True)
    slack_user = models.CharField(max_length=50, unique=True, blank=True, null=True)
    response_url = models.URLField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
    

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(blank=False, null=False, max_length=64)
    date = models.DateField(default=getLocalTime, null=False)

    def total_work_hour(self):
        check_out = self.check_out.all()
        check_in = self.check_in.all()
        date = datetime.date(1, 1, 1)

        total = datetime.timedelta(0)
        for i in range(check_out.count()):
            start_time = check_in[i].time
            stop_time = check_out[i].time
            datetime1 = datetime.datetime.combine(date, start_time)
            datetime2 = datetime.datetime.combine(date, stop_time)
            time_elapsed = datetime2 - datetime1

            total = total + time_elapsed    

        return str(total).split('.')[0]

    def is_checked_out(self):
        return self.check_in.count() == self.check_out.count()        

    def can_check_in(self):
        return self.is_checked_out()
    
    def can_check_out(self):
        return self.check_in.count() > self.check_out.count()

    def __str__(self) -> str:
        return self.name

class CheckIn(models.Model):
    timesheet = models.ForeignKey(Timesheet, blank=False, null=False, on_delete=models.CASCADE, related_name='check_in')
    time = models.TimeField(default=getLocalTime, blank=False, null=False)
    message = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.timesheet.name

class CheckOut(models.Model):
    timesheet = models.ForeignKey(Timesheet, blank=False, null=False, on_delete=models.CASCADE, related_name='check_out')
    time = models.TimeField(default=getLocalTime, blank=False, null=False, editable=True)
    message = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.timesheet.name

class SlackPayload(models.Model):
    token = models.CharField(max_length=64, blank=False, null=True)
    team_id = models.CharField(max_length=32, blank=False, null=True)
    team_domain = models.CharField(max_length=64, blank=False, null=True)
    channel_id = models.CharField(max_length=64, blank=False, null=True)
    channel_name = models.CharField(max_length=32, blank=False, null=True)
    user_id = models.CharField(max_length=64, blank=False, null=True)
    user_name = models.CharField(max_length=64, blank=False, null=True)
    command = models.CharField(max_length=32, blank=False, null=True)
    text = models.CharField(max_length=64, blank=True, null=True)
    api_app_id = models.CharField(max_length=64, blank=False, null=True)
    is_enterprise_install = models.BooleanField(default=False)
    response_url = models.URLField(blank=False, null=True)
    trigger_id = models.CharField(max_length=128, blank=False, null=True)
    created_on = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self) -> str:
        return self.user_name
