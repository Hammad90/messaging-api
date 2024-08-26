from rest_framework.serializers import ModelSerializer
from .models import Messages

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = ['id', 'user_id', 'group_id', 'chat_id', 'message_type', 'content', 'sent_at', 'delivered_at', 'seen_at', 'created_at', 'updated_at']
