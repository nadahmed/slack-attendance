import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from attendance.models import CheckIn, CheckOut

def send_msg_to_slack(action, name):
    msg = ''
    if action == 'punch_in':
        msg = "<@{}> has *punched in*!".format(name)
    elif action == 'punch_out':
        msg = "<@{}> has *punched out*!".format(name)
    headers = {'Authorization': 'Bearer {}'.format(settings.SLACK_OAUTH_TOKEN)}
    return requests.post(
        settings.SLACK_WEBHOOKS_URL,
        headers=headers,
        json={
            "channel": 'C02AQL83XQB',
            "text": msg
        })

@receiver(post_save, sender=CheckIn)
def checkin_callback(sender, instance, created, **kwargs):
    if created:
        try:
            send_msg_to_slack('punch_in', instance.timesheet.user.slack.slack_id)
        except:
            pass
        times = instance.timesheet.check_in.all()
        if times.count() == 1:
            current_time = times.first().time
            reporting_time = instance.timesheet.user.shift.shift.from_time
            if (reporting_time < current_time):
                instance.timesheet.is_late = True
                instance.timesheet.save(update_fields=['is_late'])


@receiver(post_save, sender=CheckOut)
def checkout_callback(sender, instance, created, **kwargs):
    if created:
        try:
            send_msg_to_slack('punch_out', instance.timesheet.user.slack.slack_id)
        except:
            pass