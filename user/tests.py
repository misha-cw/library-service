from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from user.serializers import UserSerializer

CREATE_USER_URL = reverse("user:create")
MANAGE_USER_URL = reverse("user:manage")
USER = get_user_model()


class CreateUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        payload = {"email": "user@test.com", "password": "userpass123"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(USER.objects.filter(email=payload["email"]).exists())
        user = USER.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))


class UnauthenticatedManageUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(MANAGE_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedManageUserApiTest(TestCase):
    def setUp(self):
        self.user = USER.objects.create_user(
            email="user@test.com", password="userpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        res = self.client.get(MANAGE_USER_URL)
        serializer = UserSerializer(self.user)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_user(self):
        payload = {
            "email": "updated@test.com",
            "password": "updatedpass123",
        }
        res = self.client.put(MANAGE_USER_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_partial_update_user(self):
        payload = {
            "email": "updated@test.com",
        }

        res = self.client.patch(MANAGE_USER_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload["email"])
