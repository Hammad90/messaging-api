from rest_framework.serializers import ModelSerializer
from .models import Messages

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
