from unittest.mock import Mock, patch

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from urlshortener.shortener.models import Shortener
from urlshortener.shortener.selectors import get_long_url


class GetLongUrlTests(TestCase):
    def setUp(self):
        self.short_url = "short1"
        self.long_url = "http://example.com/long"
        self.snowflake_id = "1234567890"
        self.cache_key = f"short_url:{self.short_url}"
        self.shortener = Shortener.objects.create(
            snowflake_id=self.snowflake_id,
            short_url=self.short_url,
            long_url=self.long_url,
        )
        cache.clear()

    def test_get_long_url_cache_hit(self):
        # Simulate cache hit
        cache.set(self.cache_key, self.long_url, timeout=60 * 60)
        result = get_long_url(short_url=self.short_url)
        self.assertEqual(result, self.long_url)

    @patch("urlshortener.shortener.selectors.Shortener.objects.filter")
    def test_get_long_url_cache_miss_db_hit(self, mock_filter):
        # Simulate cache miss and database hit
        cache.delete(self.cache_key)
        mock_shortener = Mock()
        mock_shortener.long_url = self.long_url
        mock_filter.return_value.first.return_value = mock_shortener

        result = get_long_url(short_url=self.short_url)
        self.assertEqual(result, self.long_url)
        self.assertEqual(cache.get(self.cache_key), self.long_url)

    @patch("urlshortener.shortener.selectors.Shortener.objects.filter")
    def test_get_long_url_cache_miss_db_miss(self, mock_filter):
        # Simulate cache miss and database miss
        cache.delete(self.cache_key)
        mock_filter.return_value.first.return_value = None

        with self.assertRaises(ObjectDoesNotExist):
            get_long_url(short_url=self.short_url)

    def test_get_long_url_db_exception(self):
        # Simulate database exception
        with patch.object(Shortener.objects, "filter", side_effect=Shortener.DoesNotExist):
            with self.assertRaises(ObjectDoesNotExist):
                get_long_url(short_url=self.short_url)
