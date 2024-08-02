from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from urlshortener.users.models import BaseUser


class UserCreateApiTests(APITestCase):
    def setUp(self):
        self.create_url = reverse("api:users:create")
        self.valid_user_data = {
            "email": "test_user@email.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
        }

    def test_create_user_with_valid_data(self):
        response = self.client.post(self.create_url, self.valid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BaseUser.objects.count(), 1)
        self.assertEqual(BaseUser.objects.get().email, self.valid_user_data["email"])

    def test_create_user_with_missing_email(self):
        data = {"password": "Password123!", "confirm_password": "Password123!"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data['detail'])

    def test_create_user_with_invalid_email(self):
        data = {"email": "invalidemail", "password": "Password123!", "confirm_password": "Password123!"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data['detail'])

    def test_create_user_with_missing_password(self):
        data = {"email": "test_user2@email.com", "confirm_password": "Password123!"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data['detail'])

    def test_create_user_with_non_matching_passwords(self):
        data = {
            "email": "test_user3@email.com",
            "password": "Password123!",
            "confirm_password": "DifferentPassword123!",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data['detail'])

    def test_create_user_with_weak_password(self):
        data = {"email": "test_user4@email.com", "password": "weakpass", "confirm_password": "weakpass"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data['detail'])

    def test_create_user_with_duplicate_email(self):
        BaseUser.objects.create_user(email="duplicate_user@email.com", password="Password123!")
        data = {"email": "duplicate_user@email.com", "password": "Password123!", "confirm_password": "Password123!"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['detail'])
