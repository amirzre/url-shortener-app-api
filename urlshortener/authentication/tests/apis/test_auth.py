from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from urlshortener.users.models import BaseUser


class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(email="test@email.com", password="password123")
        self.login_url = reverse("api:authentication:jwt:login")
        self.refresh_url = reverse("api:authentication:jwt:refresh")
        self.verify_url = reverse("api:authentication:jwt:verify")
        self.me_url = reverse("api:authentication:me")

    def test_login_with_valid_credentials(self):
        data = {"email": "test@email.com", "password": "password123"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        data = {"email": "test@email.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}
        response = self.client.post(self.refresh_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_token(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        data = {"token": access_token}
        response = self.client.post(self.verify_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_user_me_with_valid_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_access_user_me_without_token(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
