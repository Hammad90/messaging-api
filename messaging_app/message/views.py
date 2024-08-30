from rest_framework.viewsets import ModelViewSet
from .models import Messages
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import MessageSerializer
from user.models import Users
from chat.models import Chats
from  group.models import Groups
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from logging import getLogger

logger = getLogger(__name__)

class MessageViewSet(ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'])
    def get_messages(sef, request: Request):
        user_id = request.query_params.get('user_id')
        channel_id = request.query_params.get('channel_id')
        group_messages = Messages.objects.filter(group_id=channel_id)
        print(f"Group: {len(group_messages)}")
        chat_messages = Messages.objects.filter(chat_id=channel_id)
        print(f"Chat: {len(chat_messages)}")
        messages = group_messages | chat_messages
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_message(self, request: Request):
        user_id = request.data.get('user_id')
        logger.info("=======================================")
        logger.info(f"User id: {user_id}")
        channel_id = request.data.get('channel_id')
        content = request.data.get('content')
        type = request.data.get('type')
        user = Users.objects.get(id=user_id)
        logger.info(f"User object: {user}")
        if Groups.objects.filter(id=channel_id).exists():
            group = Groups.objects.get(id=channel_id)
            message = Messages.objects.create(
                user=user,
                group=group,
                content=content,
                message_type=type
            )
        elif Chats.objects.filter(id=channel_id).exists():
            chat = Chats.objects.get(id=channel_id)
            message = Messages.objects.create(
                user=user,
                chat=chat,
                content=content,
                message_type=type
            )
        else:
            return Response({'status': 'Invalid Channel Id'}, HTTP_400_BAD_REQUEST)
        return Response({'status': 'message sent'}, status=HTTP_200_OK)
            