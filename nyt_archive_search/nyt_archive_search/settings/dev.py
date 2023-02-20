from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%8rz0hzi7t10fu6kznfgho!pfkx^nje2j25e9b67#v1vwl8z%c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = [
    "https://www.zebbecker.com",
    "https://*.159.203.178.166",
    "https://*.127.0.0.1",
]