from django.db import models
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone

User = get_user_model()

class LeaveType(models.Model):
    pass
    name = models.CharField(max_length=64)
    count = models.SmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Leave Type"
    

class LeaveForm(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='leave_form')
    date_from = models.DateField(verbose_name="From")
    date_to = models.DateField(null=True, blank=True, verbose_name="Till")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.RESTRICT)
    reason = models.CharField(max_length=255)
    
    def leave_count(self):
        if self.date_to is not None and self.date_to > self.date_from:
            return (self.date_to - self.date_from).days
        else:
            datetime.timedelta(1).days

    # def notify_supervisor(self):
    #     print("Notified Supervisor!")

    def __str__(self):
        return "{} - {}".format(self.leave_type.name, self.applicant.username)
    
def get_local_time():
    return timezone.localtime(timezone.now())

class Approval(models.Model):
    
    APPROVAL_TYPES = (
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
    )
    
    approval_type = models.CharField(max_length=20, choices=APPROVAL_TYPES, default='pending')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateField(editable=False, default=get_local_time)
    modified = models.DateTimeField(default=get_local_time)
    leave_form = models.OneToOneField(LeaveForm, on_delete=models.CASCADE, blank=False, null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = get_local_time()
        self.modified = get_local_time()
        return super(Approval, self).save(*args, **kwargs)

    def __str__(self):
        return self.approval_type
    