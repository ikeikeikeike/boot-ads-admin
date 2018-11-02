from ads.settings import *  # NOQA
from ads.settings import (
    INSTALLED_APPS,
    MIDDLEWARE,
    #  TEMPLATES,
    ETH0_ADDR
)


DEBUG = True
ENVIRONMENT = 'local'
CSRF_COOKIE_SECURE = False
#  TEMPLATES[0]['OPTIONS']['constants'].update({'DEBUG': DEBUG})


INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    ETH0_ADDR
]


INSTALLED_APPS = INSTALLED_APPS + [
    'django_extensions',
]


MIDDLEWARE = MIDDLEWARE + []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ads_development',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    },
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-location'
    },
    'lock_in_task': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lock_in_task-location'
    },
}
