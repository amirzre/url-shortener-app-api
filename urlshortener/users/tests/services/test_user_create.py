from django.core.exceptions import ValidationError
from django.test import TestCase

from urlshortener.users.models import BaseUser
from urlshortener.users.services import user_create


class UserCreateTests(TestCase):
    def test_user_without_password_is_created_with_unusable_one(self):
        user = user_create(email="random_user@email.com")

        self.assertFalse(user.has_usable_password())

    def test_user_with_capitalized_email_cannot_be_created(self):
        user_create(email="random_user@email.com")

        with self.assertRaises(ValidationError):
            user_create(email="RANDOM_user@email.com")

        self.assertEqual(1, BaseUser.objects.count())
    
    def test_user_with_valid_data_is_created(self):
        user = user_create(
            email="valid_user@email.com",
            password="securepassword123",
        )
        
        self.assertEqual(user.email, "valid_user@email.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
    
    def test_user_with_blank_email_raises_error(self):
        with self.assertRaises(ValueError):
            user_create(email="", password="password")
    
    def test_user_with_duplicate_email_raises_error(self):
        user_create(email="unique_user@email.com")
        with self.assertRaises(ValidationError):
            user_create(email="unique_user@email.com")
        
        self.assertEqual(1, BaseUser.objects.count())

    def test_user_created_with_is_active_false(self):
        user = user_create(
            email="inactive_user@email.com",
            password="securepassword123",
            is_active=False
        )
        
        self.assertFalse(user.is_active)
    
    def test_user_created_with_is_admin_true(self):
        user = user_create(
            email="admin_user@email.com",
            password="securepassword123",
            is_admin=True
        )

        self.assertTrue(user.is_admin)

    def test_user_created_with_is_admin_false(self):
        user = user_create(
            email="normal_user@email.com",
            password="securepassword123",
        )

        self.assertFalse(user.is_admin)
    
    def test_user_with_invalid_email_raises_error(self):
        invalid_emails = ["invalid", "invalid@", "invalid.com", "@invalid.com"]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                user_create(email=email)
