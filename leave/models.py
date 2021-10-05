from django.db import models
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=64)
    count = models.SmallIntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
    

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='leave_applications')
    date_from = models.DateField(verbose_name="From")
    date_to = models.DateField(null=True, blank=True, verbose_name="Till")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name="Leave type")
    reason = models.CharField(max_length=255)
    
    def total_days(self):
        if self.date_to is not None and self.date_to > self.date_from:
            return (self.date_to - self.date_from).days
        else:
            datetime.timedelta(1).days

    def notify_supervisor(self):
        print("Notified Supervisor!")

    # def __str__(self):
    #     return self.name.username
    
class Approval(models.Model):
    APPROVAL_TYPES = (
        ('final', 'Final'),
        ('forward', 'Forward')
    )
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    approved_on = models.DateTimeField(blank= True, null=True)
    next_approval = models.OneToOneField('Approval', on_delete=models.SET_NULL, null=True, blank=True)
    approval_type = models.CharField(max_length=20, choices=APPROVAL_TYPES, default='final')
    

    # def __str__(self):
    #     return self.application.name.username
    