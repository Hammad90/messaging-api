from os import getenv

from openai import OpenAI
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import Users

from .models import Chats
from .serializers import ChatSerializer


class CreateChatAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        member_ids = request.data.get("member_ids")

        if not member_ids:
            return Response(
                {"error": "Member ids is required"}, status=HTTP_400_BAD_REQUEST
            )
        members = []
        if len(member_ids) > 2:
            return Response(
                {"error": "Chat can only have 2 members"}, status=HTTP_400_BAD_REQUEST
            )
        for user_id in member_ids:
            try:
                user = Users.objects.get(id=user_id)
                members.append(user)
            except Users.DoesNotExist:
                return Response(
                    {"error": "User does not exist"}, status=HTTP_404_NOT_FOUND
                )
        chat = Chats.objects.create()
        chat.members.set(members)

        serializer = ChatSerializer(chat)
        return Response(serializer.data, status=HTTP_201_CREATED)


class DeleteChatAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request: Request, chat_id: int):
        try:
            chat = Chats.objects.get(id=chat_id)
            chat.delete()
            return Response(
                {"status": "Chat deleted successfully"}, status=HTTP_204_NO_CONTENT
            )
        except Chats.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=HTTP_404_NOT_FOUND)


class GptChatAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request: Request):
        openai_client = OpenAI(api_key=getenv("OPENAI_API_KEY"))
        prompt = request.data.get("prompt")
        response = openai_client.chat.completions.create(
            model="gpt-3", messages=[{"role": "user", "content": prompt}]
        )
        answer = response["choices"][0]["message"]["content"]
        return Response({"answer": answer}, status=HTTP_200_OK)
