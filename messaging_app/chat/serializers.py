from rest_framework.serializers import ModelSerializer
from .models import Chats

class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chats
        fields = ['id', 'name', 'created_at', 'updated_at']
