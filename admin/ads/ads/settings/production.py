import os

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


LOGGING['handlers']['syslog'] = {
    'level': 'INFO',
    'class': 'logging.handlers.SysLogHandler',
    'address': '/dev/log',
    'formatter': 'syslog_verbose',
}

LOGGING['handlers']['syslog_error'] = {
    'level': 'INFO',
    'filters': ['require_debug_false'],
    'class': 'logging.handlers.SysLogHandler',
    'address': '/dev/log',
    'formatter': 'syslog_verbose',
}

LOGGING['loggers']['syslog'] = {
    'handlers': ['syslog', 'console', 'syslog_error'],
    'level': 'INFO',
    'propagate': False,
}

LOGGING['loggers'][''] = {
    'handlers': ['console', 'syslog_error'],
    'level': 'INFO',
    'propagate': True
}

LOGGING['loggers']['django']['level'] = 'INFO'
LOGGING['loggers']['django.db.backends']['level'] = 'INFO'
LOGGING['loggers'][LOGGING_PREFIX]['level'] = 'INFO'

LOGGING['loggers']['django']['handlers'].append("syslog_error")
LOGGING['loggers']['django.db.backends']['handlers'].append("syslog_error")
LOGGING['loggers'][LOGGING_PREFIX]['handlers'].append("syslog_error")
