from django.urls import path

from .views import GetMessagesAPIView, SendMessageAPIView

urlpatterns = [
    path("messages/send/", SendMessageAPIView.as_view(), name="send_message"),
    path("messages/get/", GetMessagesAPIView.as_view(), name="get_messages"),
]
