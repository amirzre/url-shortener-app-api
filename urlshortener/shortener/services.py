from typing import Tuple

from urlshortener.shortener.models import Shortener
from urlshortener.utils.encode_base62 import encode_base62
from urlshortener.utils.snowflake import SnowflakeIDGenerator


def create_or_get_short_url(*, long_url: str) -> Tuple[Shortener, bool]:
    existing_short_url = Shortener.objects.filter(long_url=long_url).first()
    if existing_short_url:
        return existing_short_url, False

    generator = SnowflakeIDGenerator(datacenter_id=1, machine_id=1)
    snowflake_id = generator.generate_id()

    short_url = encode_base62(snowflake_id)

    shortener = Shortener(snowflake_id=snowflake_id, short_url=short_url, long_url=long_url)
    shortener.save()
    return shortener, True
