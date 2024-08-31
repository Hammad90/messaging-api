from django.urls import path, include
from .views import SendMessageAPIView, GetMessagesAPIView

urlpatterns = [
    path('messages/send/', SendMessageAPIView.as_view(), name='send_message'),
    path('messages/get/', GetMessagesAPIView.as_view(), name='get_messages')
]
