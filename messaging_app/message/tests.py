from core.tests import BaseTestCase
from django.urls import reverse
from rest_framework.status import HTTP_200_OK


class MessagesTestCase(BaseTestCase):

    def test_get_message(self):
        self.authenticate_user_1()
        url = reverse("get_messages")
        response = self.client.get(f"{url}?user_id={self.user_1.id}")
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_send_message_to_group(self):
        self.authenticate_user_2()
        join_group_url = reverse("join_group")
        response = self.client.post(
            join_group_url,
            {"user_id": self.user_2.id, "group_id": self.group.id},
            format="json",
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        send_message_url = reverse("send_message")
        response = self.client.post(
            send_message_url,
            {
                "user_id": self.user_2.id,
                "group_id": self.group.id,
                "content": "test message",
                "message_type": "text",
            },
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_send_message_to_chat(self):
        self.authenticate_user_1()

        send_message_url = reverse("send_message")
        response = self.client.post(
            send_message_url,
            {
                "user_id": self.user_1.id,
                "chat_id": self.chat.id,
                "content": "test message",
                "message_type": "text",
            },
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
