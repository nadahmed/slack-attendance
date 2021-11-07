from rest_framework import routers
from leave.views import LeaveTypeViewSet, LeaveFormViewSet

router = routers.SimpleRouter()
router.register(r'leavetypes', LeaveTypeViewSet)
router.register(r'leaveforms', LeaveFormViewSet)

urlpatterns = []

urlpatterns += router.urls