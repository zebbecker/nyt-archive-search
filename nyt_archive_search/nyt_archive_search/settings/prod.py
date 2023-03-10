import os
from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "159.203.178.166", "zebbecker.com", "www.zebbecker.com"]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

CSRF_TRUSTED_ORIGINS = ["https://www.zebbecker.com", "https://159.203.178.166"]
