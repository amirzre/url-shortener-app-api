from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import ShortUrl


class AdminSiteTests(TestCase):
    """Tests for admin panel page"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@email.com',
            password='testpass',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@email.com',
            password='testpass',
            name='fullname',
        )
        self.shorturl = ShortUrl.objects.create(
            url='http://127.0.0.1:8000/api/list/',
            short_id='Err2tY',
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_delete_user_page(self):
        """Test that the delete user page works"""
        url = reverse('admin:core_user_delete', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_short_url_listed(self):
        """Test that urls are listed on shorturls page"""
        url = reverse('admin:core_shorturl_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.shorturl.url)
        self.assertContains(res, self.shorturl.short_id)

    def test_short_url_change_page(self):
        """Test that the shorturl edit page works"""
        url = reverse('admin:core_shorturl_change', args=[self.shorturl.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_short_url_page(self):
        """Test that the create short url page works"""
        url = reverse('admin:core_shorturl_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_delete_short_url_page(self):
        """Test that the delete short url page works"""
        url = reverse('admin:core_shorturl_delete', args=[self.shorturl.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
