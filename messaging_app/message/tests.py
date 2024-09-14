from chat.models import Chats
from django.urls import reverse
from group.models import Groups
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient, APITestCase
from user.models import Users


class MessagesTestCase(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(
            username="testuser1",
            password="testpassword",
            email="test@example.com",
            first_name="test",
            last_name="last",
        )
        self.user2 = Users.objects.create(
            username="testuser2",
            password="testpassword",
            email="test2@example.com",
            first_name="test",
            last_name="last",
        )
        self.group = Groups.objects.create(
            name="group1", description="test group", created_by=self.user
        )
        self.chat = Chats.objects.create()
        self.user.set_password("testpassword")
        self.user2.set_password("testpassword")
        self.chat.members.set([self.user, self.user2])
        self.user.save()
        self.user2.save()
        self.group.save()
        self.chat.save()
        self.user_id = self.user.id
        self.group_id = self.group.id
        self.chat_id = self.chat.id
        self.client = APIClient()

    def authenticate(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": "testuser1", "password": "testpassword"}, format="json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_get_message(self):
        self.authenticate()
        url = reverse("get_messages")
        response = self.client.get(f"{url}?user_id={self.user_id}")
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_send_message_to_group(self):
        self.authenticate()
        join_group_url = reverse("join_group")
        response = self.client.post(
            join_group_url,
            {"user_id": self.user_id, "group_id": self.group_id},
            format="json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        send_message_url = reverse("send_message")
        response = self.client.post(
            send_message_url,
            {
                "user_id": self.user_id,
                "group_id": self.group_id,
                "content": "test message",
                "message_type": "text",
            },
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_send_message_to_chat(self):
        self.authenticate()
        send_message_url = reverse("send_message")
        response = self.client.post(
            send_message_url,
            {
                "user_id": self.user_id,
                "chat_id": self.chat_id,
                "content": "test message",
                "message_type": "text",
            },
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
