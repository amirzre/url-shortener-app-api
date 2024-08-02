from unittest.mock import MagicMock, patch

import pytest

from urlshortener.shortener.models import Shortener
from urlshortener.shortener.services import create_or_get_short_url


@pytest.mark.django_db
class TestCreateOrGetShortUrl:
    @patch("urlshortener.shortener.models.Shortener.objects.filter")
    def test_existing_short_url(self, mock_filter):
        long_url = "https://example.com"
        mock_shortener_instance = MagicMock(spec=Shortener)
        mock_shortener_instance.long_url = long_url
        mock_shortener_instance.short_url = "abc123"
        mock_filter.return_value.first.return_value = mock_shortener_instance

        shortener, created = create_or_get_short_url(long_url=long_url)

        assert shortener == mock_shortener_instance
        assert not created
        mock_filter.assert_called_once_with(long_url=long_url)
        mock_filter.return_value.first.assert_called_once()

    @patch("urlshortener.shortener.services.SnowflakeIDGenerator")
    @patch("urlshortener.shortener.services.encode_base62")
    @patch("urlshortener.shortener.models.Shortener.objects.filter")
    def test_create_new_short_url(self, mock_filter, mock_encode_base62, mock_snowflake):
        with patch.object(Shortener, "save", MagicMock()) as mock_save:
            # Arrange
            long_url = "https://newexample.com"
            mock_filter.return_value.first.return_value = None
            mock_snowflake_instance = mock_snowflake.return_value
            mock_snowflake_instance.generate_id.return_value = 123456789
            mock_encode_base62.return_value = "newabc123"

            shortener, created = create_or_get_short_url(long_url=long_url)

            assert created
            assert shortener.short_url == "newabc123"
            assert shortener.long_url == long_url
            assert shortener.snowflake_id == 123456789

            mock_filter.assert_called_once_with(long_url=long_url)
            mock_filter.return_value.first.assert_called_once()
            mock_snowflake.assert_called_once_with(datacenter_id=1, machine_id=1)
            mock_snowflake_instance.generate_id.assert_called_once()
            mock_encode_base62.assert_called_once_with(123456789)
            mock_save.assert_called_once()
