import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import F

User = get_user_model()

def getLocalTime():
    return timezone.localtime(timezone.now())

# class AccessPermission(models.Model):
#     user = models.ManyToManyField(User, related_name='access_permissions')
#     code = models.CharField(max_length=100, unique=True)
    
#     def __str__(self) -> str:
#         return self.code

class SlackUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="slack", unique=True)
    slack_id = models.CharField(max_length=50, unique=True)
    response_url = models.URLField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.user.username
    
def get_default_user():
    return User.objects.all().first().id

class Shift(models.Model):
    CHOICES = (
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    )
    name = models.CharField(max_length=50, unique=True)
    from_time = models.TimeField(verbose_name='From')
    to_time = models.TimeField(verbose_name='To')
    buffer_time = models.PositiveIntegerField(default=15, help_text="Buffer time in minutes")
    is_active = models.BooleanField(default=True)
    work_days = models.PositiveIntegerField(default=5)
    day_of_the_week= models.PositiveIntegerField("Day of the week", choices=CHOICES, default=0)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                temp = Shift.objects.get(is_default=True)
                if self != temp:
                    temp.is_default= False
                    temp.save()
            except Shift.DoesNotExist:
                pass
        super(Shift, self).save(*args, **kwargs)

    class Meta:
        unique_together = ['from_time', 'to_time', 'buffer_time']
        ordering = ['id']

class ShiftUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shift")
    shift = models.ForeignKey(Shift, on_delete=models.RESTRICT, related_name="users")

    class Meta:
        unique_together = ['user', 'shift']

class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    date = models.DateField(default=getLocalTime, null=False)
    is_late = models.BooleanField(default=False)

    @classmethod
    def get_or_create_for_today(cls, user):
        (sheet, created) =  cls.objects.get_or_create(user=user, date=getLocalTime().today().date())
        return sheet

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

        # return str(total).split('.')[0]
        return total


    def is_checked_out(self):
        return self.check_in.count() == self.check_out.count()        

    def can_check_in(self):
        return self.is_checked_out()
    
    def can_check_out(self):
        return self.check_in.count() > self.check_out.count()

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        ordering = ['-date']

class CheckIn(models.Model):
    timesheet = models.ForeignKey(Timesheet, blank=False, null=False, on_delete=models.CASCADE, related_name='check_in')
    time = models.TimeField(default=getLocalTime, blank=False, null=False)
    message = models.CharField(max_length=500, blank=True, null=True)
            
    def __str__(self) -> str:
        return self.timesheet.user.username
    
    class Meta:
        ordering = ['time']

class CheckOut(models.Model):
    timesheet = models.ForeignKey(Timesheet, blank=False, null=False, on_delete=models.CASCADE, related_name='check_out')
    time = models.TimeField(default=getLocalTime, blank=False, null=False)
    message = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:
        return self.timesheet.user.username

    class Meta:
        ordering = ['time']

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
