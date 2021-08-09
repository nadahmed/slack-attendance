from django.db import models
from django.forms import ModelForm
from .models import SlackPayload

class SlackPayloadForm(ModelForm):
    class Meta:
        model = SlackPayload
        exclude = ['created_on']