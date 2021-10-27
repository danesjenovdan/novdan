import os

from .base import *

# generate with
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'secret_key_changeme')

DEBUG = bool(os.getenv('DJANGO_DEBUG', False))

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'api.novdan.lb.djnd.si']

STATIC_ROOT = os.getenv('DJANGO_STATIC_ROOT', BASE_DIR / 'static')
STATIC_URL = os.getenv('DJANGO_STATIC_URL_BASE', '/static/')
MEDIA_ROOT = os.getenv('DJANGO_MEDIA_ROOT', BASE_DIR / 'media')
MEDIA_URL = os.getenv('DJANGO_MEDIA_URL_BASE', '/media/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DJANGO_DATABASE_HOST', 'host_changeme'),
        'PORT': os.getenv('DJANGO_DATABASE_PORT', '5432'),
        'NAME': os.getenv('DJANGO_DATABASE_NAME', 'name_changeme'),
        'USER': os.getenv('DJANGO_DATABASE_USERNAME', 'username_changeme'),
        'PASSWORD': os.getenv('DJANGO_DATABASE_PASSWORD', 'password_changeme'),
    }
}

if os.getenv('DJANGO_ENABLE_S3', False):
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID', 'key_id_changeme')
    AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY', 'access_key_changeme')
    AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME', 'djnd')
    AWS_DEFAULT_ACL = 'public-read' # if files are not public they won't show up for end users
    AWS_QUERYSTRING_AUTH = False # query strings expire and don't play nice with the cache
    AWS_LOCATION = os.getenv('DJANGO_AWS_LOCATION', 'novdan-api')
    AWS_S3_REGION_NAME = os.getenv('DJANGO_AWS_REGION_NAME', 'fr-par')
    AWS_S3_ENDPOINT_URL = os.getenv('DJANGO_AWS_S3_ENDPOINT_URL', 'https://s3.fr-par.scw.cloud')
    AWS_S3_SIGNATURE_VERSION = os.getenv('DJANGO_AWS_S3_SIGNATURE_VERSION', 's3v4')
