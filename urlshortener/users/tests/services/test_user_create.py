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
