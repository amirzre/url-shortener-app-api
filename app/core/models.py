import random
import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email insted of username"""
    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_('Email')
    )
    name = models.CharField(
        max_length=255, verbose_name=_('Full Name')
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_('Is Active?')
    )
    is_staff = models.BooleanField(
        default=False, verbose_name=_('Is Staff?')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'


class ShortUrl(models.Model):
    ID_LENGTH = 6
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shorturls',
        blank=True,
        null=True,
        verbose_name=_('User')
    )
    short_id = models.CharField(
        max_length=ID_LENGTH,
        unique=True,
        blank=False,
        verbose_name=_('Short URL')
    )
    url = models.URLField(blank=False, verbose_name=_('Original URL'))
    count = models.PositiveIntegerField(default=0, verbose_name=_('Count'))
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created Time')
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated Time')
    )

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.short_id} - {self.url}'

    def increase_short_id_counter(self):
        """When a user request a original url with the short_id."""
        self.count += 1
        self.save()

    @classmethod
    def generate_short_id(cls):
        """
        Generate a short id used to shorten the original url
        making sure short id is not in used.
        """

        CHARACTERS = (
            string.ascii_lowercase
            + string.ascii_uppercase
            + string.digits
        )

        while True:
            short_id = ''.join(
                random.choice(CHARACTERS)
                for _ in range(cls.ID_LENGTH)
            )

            try:
                cls.objects.get(short_id=short_id)
            except ObjectDoesNotExist:
                return short_id
