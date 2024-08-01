from django.db import models

from urlshortener.common.models import BaseModel


class Shortener(BaseModel):
    snowflake_id = models.BigIntegerField(unique=True)
    short_url = models.CharField(max_length=50, unique=True, db_index=True)
    long_url = models.URLField(unique=True)

    def __str__(self) -> str:
        return self.long_url
