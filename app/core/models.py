from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext as _

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
