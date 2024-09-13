from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APIClient, APITestCase

from .models import Users
from .views import UserViewSet


class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="test",
            last_name="last",
        )
        self.client = APIClient()
        self.user_list_url = reverse("user-list")
        print("%s", self.user_list_url)

    def test_create(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newemail@example.com",
            "first_name": "new",
            "last_name": "user",
        }
        UserViewSet.authentication_classes = []
        UserViewSet.permission_classes = []
        response = self.client.post(self.user_list_url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(
            Users.objects.get(username="newuser").email, "newemail@example.com"
        )
