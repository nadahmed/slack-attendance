import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import CheckIn, CheckOut

def send_msg_to_slack(action, name):
    msg = ''    
    if action == 'punch_in':
        msg = "{} has punched in!".format(name)
    elif action == 'punch_out':
        msg = "{} has punched out!".format(name)
    headers = {'Authorization': 'Bearer %s' % settings.SLACK_OAUTH_TOKEN}
    return requests.post(
        settings.SLACK_WEBHOOKS_URL,
        headers=headers,
        json={
            "channel": 'C02AQL83XQB',
            "text": msg
        })

@receiver(post_save, sender=CheckIn)
def my_callback(sender, instance, created, **kwargs):
    if created:
        send_msg_to_slack('punch_in', instance.timesheet.user.slack.name)

@receiver(post_save, sender=CheckOut)
def my_callback(sender, instance, created, **kwargs):
    if created:
        send_msg_to_slack('punch_out', instance.timesheet.user.slack.name)