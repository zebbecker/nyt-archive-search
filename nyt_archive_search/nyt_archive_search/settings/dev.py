from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%8rz0hzi7t10fu6kznfgho!pfkx^nje2j25e9b67#v1vwl8z%c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["DJANGO_EMAIL_HOST"]
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["DJANGO_EMAIL_USER"]
EMAIL_HOST_PASSWORD = os.environ["DJANGO_EMAIL_PASSWORD"]
