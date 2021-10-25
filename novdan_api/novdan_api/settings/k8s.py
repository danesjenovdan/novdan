import os

from .base import *

# generate with
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'thisshouldbesecret')

DEBUG = bool(os.getenv('DJANGO_DEBUG', False))

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', '/static/')
STATIC_URL = os.getenv('DJANGO_STATIC_URL_BASE', '/static/')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', '/media/')
MEDIA_URL = os.getenv('DJANGO_MEDIA_URL_BASE', '/media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DATABASE_NAME', 'novdan'),
        'USER': os.getenv('DJANGO_DATABASE_USERNAME', 'user_changeme'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', 'pass_changeme'),
        'HOST': os.getenv('DJANGO_DATABASE_HOST', 'db'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', '5432'),
    }
}
