from django.urls import path
from .views import Payload


urlpatterns = [
    path("slack/test/", Payload.as_view(), name="test"),
    path("slack/in/", Payload.as_view(), name="in"),
    path("slack/out/", Payload.as_view(), name="out")
]
