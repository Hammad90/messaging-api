from chat.models import Chats
from django.urls import reverse
from group.models import Groups
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient, APITestCase
from user.models import Users


class BaseTestCase(APITestCase):

    def setUp(self):
        self.user_1 = Users.objects.create(
            username="testuser1",
            password="testpassword",
            email="test@example.com",
            first_name="test",
            last_name="last",
        )
        self.user_2 = Users.objects.create(
            username="testuser2",
            password="testpassword",
            email="test2@example.com",
            first_name="test",
            last_name="last",
        )
        self.group = Groups.objects.create(
            name="group1", description="test group", created_by=self.user_1
        )
        self.chat = Chats.objects.create()
        self.user_1.set_password("testpassword")
        self.user_2.set_password("testpassword")
        self.chat.members.set([self.user_1, self.user_2])
        self.user_1.save()
        self.user_2.save()
        self.group.save()
        self.chat.save()
        self.client = APIClient()

    def __authenticate(self, username: str, password: str):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": username, "password": password}, format="json"
        )
        self.assertEqual(
            response.status_code, HTTP_200_OK, f"Failed to authenticate {username}"
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def authenticate_user_1(self):
        self.__authenticate(self.user_1.username, "testpassword")

    def authenticate_user_2(self):
        self.__authenticate(self.user_2.username, "testpassword")

    def join_group(self, user: Users, group: Groups):
        user_id = user.id
        group_id = group.id
        join_group_url = reverse("join_group")
        response = self.client.post(
            join_group_url,
            {"user_id": user_id, "group_id": group_id},
            format="json",
        )
        self.assertEqual(
            response.status_code,
            HTTP_200_OK,
            f"Failed to make user: {user.username} join group: {group.name}",
        )
