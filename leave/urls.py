from rest_framework import routers
from leave.views import LeaveTypeViewSet

router = routers.SimpleRouter()
router.register(r'leavetypes', LeaveTypeViewSet)

urlpatterns = []

urlpatterns += router.urls