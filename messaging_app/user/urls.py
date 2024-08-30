from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserChatViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'userchats', UserChatViewSet, basename='userchats')

urlpatterns = [
    path('', include(router.urls))
]
