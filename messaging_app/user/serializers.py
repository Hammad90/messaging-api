from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Users
from chat.models import Chats

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'name', 'phone_number', 'email', 'created_at', 'updated_at']


class UserChatSerializer(ModelSerializer):
    chats = PrimaryKeyRelatedField(queryset=Chats.objects.all(), many=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'phone_number', 'email', 'created_at', 'updated_at']

    def create(self, validated_data):
        chats_data = validated_data.pop('chats')
        user = Users.objects.create(**validated_data)
        user.chats.set(chats_data)
        return user
