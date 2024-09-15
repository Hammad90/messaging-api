from core.tests import BaseTestCase
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED

from .models import Users
from .views import UserViewSet


class UserViewSetTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.user_list_url = reverse("user-list")

    def test_create_user_without_authentication(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newemail@example.com",
            "first_name": "new",
            "last_name": "user",
        }
        response = self.client.post(self.user_list_url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 3)
        self.assertEqual(
            Users.objects.get(username="newuser").email, "newemail@example.com"
        )

    def test_create_user_with_authentication(self):
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
        self.assertEqual(Users.objects.count(), 3)
        self.assertEqual(
            Users.objects.get(username="newuser").email, "newemail@example.com"
        )
