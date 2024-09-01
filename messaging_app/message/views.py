from datetime import datetime

from chat.models import Chats
from group.models import Groups
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from user.models import Users

from .models import Messages
from .serializers import MessageSerializer


class SendMessageAPIView(APIView):
    def post(self, request: Request):
        user_id = request.data.get("user_id")
        group_id = request.data.get("group_id")
        chat_id = request.data.get("chat_id")
        content = request.data.get("content")
        message_type = request.data.get("message_type")

        if not user_id or not content or not message_type:
            return Response(
                {"error": "User id, content and message type are required fields."},
                status=HTTP_400_BAD_REQUEST,
            )

        try:
            user = Users.objects.get(id=user_id)
            group = None
            chat = None
            if group_id:
                group = Groups.objects.get(id=group_id)
            if chat_id:
                chat = Chats.objects.get(id=chat_id)
            message = Messages.objects.create(
                sent_by=user,
                group=group,
                chat=chat,
                content=content,
                message_type=message_type,
            )
            serializer = MessageSerializer(message)

            return Response(serializer.data, status=HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({"error": "User does not exist"}, status=HTTP_404_NOT_FOUND)
        except Groups.DoesNotExist:
            return Response(
                {"error": "Group does not exist"}, status=HTTP_404_NOT_FOUND
            )
        except Chats.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=HTTP_404_NOT_FOUND)


class GetMessagesAPIView(APIView):
    def get(self, request: Request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"error": "User Id is required"}, status=HTTP_400_BAD_REQUEST
            )
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "User does not exist"}, status=HTTP_404_NOT_FOUND)
        user_chats = Chats.objects.filter(members=user)
        chat_messages = Messages.objects.filter(chat__in=user_chats)

        chat_messages_to_update = chat_messages.filter(
            delivered_at__isnull=True
        ).exclude(sent_by__exact=user_id)
        chat_messages_to_update.update(delivered_at=datetime.now())

        user_groups = Groups.objects.filter(groupmembers__user=user)
        group_messages = Messages.objects.filter(group__in=user_groups)

        chat_messages_dict = {}
        group_messages_dict = {}

        for message in chat_messages:
            chat_id = message.chat.id
            if chat_id not in chat_messages_dict.keys():
                chat_messages_dict[chat_id] = []
            chat_messages_dict[chat_id].append(MessageSerializer(message).data)

        for message in group_messages:
            group_id = message.group.id
            if group_id not in group_messages_dict.keys():
                group_messages_dict[group_id] = []
            group_messages_dict[group_id].append(MessageSerializer(message).data)

        response_date = {
            "messages": {
                "chats": [
                    {"chat_id": chat_id, "messages": messages}
                    for chat_id, messages in chat_messages_dict.items()
                ],
                "groups": [
                    {"group_id": group_id, "messages": messages}
                    for group_id, messages in group_messages_dict.items()
                ],
            }
        }

        return Response(response_date, status=HTTP_200_OK)
