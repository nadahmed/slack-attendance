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
    date_from = models.DateField(verbose_name="From")
    date_to = models.DateField(null=True, blank=True, verbose_name="Till")
    name = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name="Applicant", )
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name="Leave type")
    reason = models.CharField(max_length=255)

    def total_days(self):
        if self.date_to is not None and self.date_to > self.date_from:
            return (self.date_to - self.date_from).days
        else:
            datetime.timedelta(1).days

    def __str__(self):
        return self.name.username
    
class Approval(models.Model):
    application = models.OneToOneField(Application, on_delete=models.RESTRICT, related_name='application')
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null=True)
    approved_on = models.DateTimeField(blank= True, null=True)

    def __str__(self):
        return self.application.name.username
    