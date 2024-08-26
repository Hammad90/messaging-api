from rest_framework.viewsets import ModelViewSet
from .models import Chats
from .serializers import ChatSerializer

class ChatViewSet(ModelViewSet):
    queryset = Chats.objects.all()
    serializer_class = ChatSerializer
