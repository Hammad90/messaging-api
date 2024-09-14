from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient, APITestCase

from .models import Users
from .views import UserViewSet


class UserViewSetTestCase(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(
            username="testuser1",
            password="testpassword",
            email="test@example.com",
            first_name="test",
            last_name="last",
        )
        self.user.set_password("testpassword")
        self.user.save()
        self.client = APIClient()
        self.user_list_url = reverse("user-list")
        print("%s", self.user_list_url)

    def authenticate(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": "testuser1", "password": "testpassword"}, format="json"
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_non_authenticated(self):
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newemail@example.com",
            "first_name": "new",
            "last_name": "user",
        }
        response = self.client.post(self.user_list_url, data, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(
            Users.objects.get(username="newuser").email, "newemail@example.com"
        )

    def test_create_authenticated(self):
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
