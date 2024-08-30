from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Users
from chat.models import Chats
from chat.serializers import ChatSerializer
from .serializers import UserSerializer, UserChatSerializer

class UserViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class UserChatViewSet(ModelViewSet):
    queryset = Chats.objects.all()
    serializer_class = ChatSerializer

    @action(detail=True, methods=['post'])
    def join_chat(self, request: Request, pk=None):
        user_id = request.data.get('user_id')
        chat = self.get_object()
        user = Users.objects.get(id=user_id)
        user.chats.add(chat)
        return Response(
            {'status': 'user joined chat'},
            status= HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def leave_chat(self, request: Request, pk=None):
        user_id = request.data.get('user_id')
        chat = self.get_object()
        user = Users.objects.get(id=user_id)
        user.chats.remove(chat)
        return Response(
            {'status': 'user left chat'},
            status=HTTP_200_OK
        )

