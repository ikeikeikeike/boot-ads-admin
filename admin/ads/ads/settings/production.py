import os

from google.oauth2 import service_account

from ads.settings import *  # NOQA
from ads.settings import (
    INSTALLED_APPS,
    LOGGING_PREFIX,
    MIDDLEWARE,
    LOGGING,
    #  TEMPLATES,
    ETH0_ADDR
)


DEBUG = False
ENVIRONMENT = 'production'
CSRF_COOKIE_SECURE = True
#  TEMPLATES[0]['OPTIONS']['constants'].update({'DEBUG': DEBUG})


INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    ETH0_ADDR
]


INSTALLED_APPS = INSTALLED_APPS + []


MIDDLEWARE = MIDDLEWARE + []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fabg',
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_HOST'],
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

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'fabg-storage-production'
GS_DEFAULT_ACL = 'publicRead'
GS_PROJECT_ID = os.environ['GOOGLE_PROJECT']
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_CREDENTIALS']
)

LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'WARNING',
    'propagate': True
}

LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['django.db.backends']['level'] = 'INFO'
LOGGING['loggers'][LOGGING_PREFIX]['level'] = 'INFO'
