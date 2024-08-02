from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from urlshortener.shortener.models import Shortener
from urlshortener.utils.encode_base62 import encode_base62
from urlshortener.utils.snowflake import SnowflakeIDGenerator


class ShortenerApiTests(APITestCase):
    def setUp(self):
        self.create_url = reverse("api:shortener:create_short_url")
        self.redirect_url = lambda short_url: reverse("api:shortener:redirect_short_url", args=[short_url])

        self.valid_url = "https://example.com"
        self.invalid_url = "htp://invalid-url"

        self.generator = SnowflakeIDGenerator(datacenter_id=1, machine_id=1)
        self.snowflake_id = self.generator.generate_id()
        self.short_url = encode_base62(self.snowflake_id)

        # Prepopulate with a known short URL
        self.existing_shortener = Shortener.objects.create(
            snowflake_id=self.snowflake_id, short_url=self.short_url, long_url=self.valid_url
        )

    def test_create_short_url_success(self):
        data = {"long_url": "https://test.com"}
        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)
        self.assertIn("full_short_url", response.data)

    def test_create_short_url_already_exists(self):
        data = {"long_url": self.valid_url}
        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("short_url", response.data)
        self.assertIn("full_short_url", response.data)
        self.assertEqual(response.data["short_url"], self.short_url)
        self.assertTrue(response.data["full_short_url"].startswith("http://"))

    def test_create_short_url_invalid(self):
        data = {"long_url": self.invalid_url}
        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_redirect_success(self):
        response = self.client.get(self.redirect_url(self.short_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("long_url", response.data)
        self.assertEqual(response.data["long_url"], self.valid_url)

    def test_redirect_not_found(self):
        invalid_short_url = "nonexistent"
        response = self.client.get(self.redirect_url(invalid_short_url))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_cache_long_url(self):
        # Ensure caching works by making an initial request
        response = self.client.get(self.redirect_url(self.short_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(cache.get(f"short_url:{self.short_url}"), self.valid_url)

        # Make another request to check if the cache is hit
        response = self.client.get(self.redirect_url(self.short_url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_short_url_large_input(self):
        large_url = "https://" + "a" * 2048
        data = {"long_url": large_url}
        response = self.client.post(self.create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
