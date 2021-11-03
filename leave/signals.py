
from leave.models import LeaveForm, Approval
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=LeaveForm)
def leave_form_callback(sender, instance, created, **kwargs):
    pass