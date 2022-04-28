from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import ShortUrl


class ModelTests(TestCase):
    """Tests for database models"""

    def setUp(self):
        self.data = dict(
            url='http://127.0.0.1:8000/api/list/',
            short_id='Err2tY',
        )
        self.url_obj = ShortUrl.objects.create(**self.data)

    def test_create_user_with_email_successful(self):
        """Test creating new user with an email is successful"""
        email = 'test@email.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMAIL.COM'
        user = get_user_model().objects.create_user(email, 'testpass')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@email.com',
            'testuser123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_url(self):
        url_obj = ShortUrl(**self.data)

        self.assertEqual(url_obj.url, self.data['url'])
        self.assertEqual(url_obj.short_id, self.data['short_id'])
        self.assertEqual(url_obj.count, 0)

    def test_increase_url_counter(self):
        url_obj = ShortUrl.objects.get(short_id=self.data['short_id'])

        self.assertEqual(url_obj.count, 0)
        url_obj.increase_short_id_counter()
        self.assertEqual(url_obj.count, 1)

    def test_generate_short_id(self):
        short_id = ShortUrl.generate_short_id()

        self.assertEqual(len(short_id), ShortUrl.ID_LENGTH)
