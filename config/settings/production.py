from .base import *
import os
from pathlib import Path

# Override settings for production here
DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "shagorrobidasjvai.pythonanywhere.com").split(",")

CSRF_TRUSTED_ORIGINS = [
    f"https://{host.strip()}" for host in ALLOWED_HOSTS if host.strip()
]

# SQLite for PythonAnywhere free plan
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Ensure whitenoise is in MIDDLEWARE
# Since it is already in base.py, we don't strictly need to redefine it here,
# but we follow the requested structure and handle the slice carefully to avoid duplication.
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        *[m for m in MIDDLEWARE if m != "django.middleware.security.SecurityMiddleware"]
    ]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
