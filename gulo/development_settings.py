from gulo.settings import *


ALLOWED_HOSTS = [
    '127.0.0.1',
]
SCHEME = 'http://'
CSRF_TRUSTED_ORIGINS = [SCHEME + host for host in ALLOWED_HOSTS]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
STATIC_ROOT = 'static'
STATIC_URL = '/static/'