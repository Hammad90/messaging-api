from rest_framework.viewsets import ModelViewSet
from .models import Messages
from .serializers import MessageSerializer

class MessageViewSet(ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer
