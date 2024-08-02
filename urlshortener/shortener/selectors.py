from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from urlshortener.shortener.models import Shortener


def get_long_url(*, short_url: str) -> str:
    cache_key = f"short_url:{short_url}"
    long_url = cache.get(cache_key)

    if not long_url:
        shortener = Shortener.objects.filter(short_url=short_url).first()
        if shortener:
            long_url = shortener.long_url
            cache.set(cache_key, long_url, timeout=60 * 60)
        else:
            raise ObjectDoesNotExist("Long URL not found.")

    return long_url
