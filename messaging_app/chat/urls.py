from django.urls import path
from .views import CreateChatAPIView, DeleteChatAPIView

urlpatterns = [
    path('chats/create/', CreateChatAPIView.as_view(), name='create_chat'),
    path('chats/delete/<int:chat_id>/', DeleteChatAPIView.as_view(), name='delete_chat'),
]