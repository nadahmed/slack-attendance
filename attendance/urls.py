from django.urls import path
from .views import Payload
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("slack/test/", csrf_exempt(Payload.as_view()), name="test"),
    path("slack/in/", csrf_exempt(Payload.as_view()), name="in"),
    path("slack/out/", csrf_exempt(Payload.as_view()), name="out")
]
