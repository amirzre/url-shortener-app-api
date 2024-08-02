import os
from datetime import timedelta

from config.env import BASE_DIR, env

env.read_env(os.path.join(BASE_DIR, ".env"))

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SECRET_KEY", default="*6hkpfcg66b*wr+du07m**aez!&%*5uniwf$&g17y24zx^7*2"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}
