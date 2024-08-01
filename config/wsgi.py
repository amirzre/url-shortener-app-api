"""
WSGI config for urlshortener project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

env("DJANGO_SETTINGS_MODULE", default="config.django.base")

application = get_wsgi_application()
