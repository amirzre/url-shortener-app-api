from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from rest_framework.test import APIClient
from rest_framework import status


class ShortUrlTests(TestCase):
    """Test for create short url functionality"""

    def setUp(self):
        self.shorten_url = reverse('shortener:create')
        self.data = dict(
            url='http://127.0.0.1:8000/api/list/',
        )
        self.client = APIClient()

    def test_shorten_url(self):
        response = self.client.post(
            self.shorten_url,
            data=self.data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(settings.SITE_URL, response.data['short_id'])

    def test_shorten_url_data_invalid(self):
        invalid_data = {'url': 'invalid url'}
        res = self.client.post(
            self.shorten_url,
            data=invalid_data,
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Enter a valid URL.', res.data['url'])

    def test_get_original_url(self):
        response = self.client.post(
            self.shorten_url,
            data=self.data,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(settings.SITE_URL, response.data['short_id'])
        self.assertEqual(response.data['count'], 0)

        short_id = response.data['short_id'].replace(settings.SITE_URL, '')
        url_get = f'http://localhost:8000/{short_id}'
        response_get = self.client.get(url_get)

        self.assertEqual(response_get.data['count'], 1)
        self.assertEqual(url_get.data['url'], self.data['url'])
