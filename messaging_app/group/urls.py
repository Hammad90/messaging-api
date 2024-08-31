from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, JoinGroupAPIView, LeaveGroupAPIView

router = DefaultRouter()
router.register(r"groups", GroupViewSet, basename="group")

urlpatterns = [
    path("", include(router.urls)),
    path("group/join/", JoinGroupAPIView.as_view(), name="join_group"),
    path("group/leave/", LeaveGroupAPIView.as_view(), name="leave_group"),
]
