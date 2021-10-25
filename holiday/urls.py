from django.urls.conf import path
from rest_framework import routers
from holiday.views import HolidayViewSet

router = routers.SimpleRouter()
router.register(r'holiday', HolidayViewSet, basename='holiday-year')

urlpatterns = []

urlpatterns += router.urls