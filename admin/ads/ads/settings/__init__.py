"""
Django settings for ads project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
from os.path import dirname

import netifaces as ni

pjoin = os.path.join

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = dirname(dirname(os.path.abspath(__file__)))          # ../
BASE_DIR = dirname(dirname(dirname(__file__)))                      # ../../
APP_DIR = dirname(dirname(dirname(dirname(__file__))))              # ../../../
REPO_DIR = dirname(dirname(dirname(dirname(dirname(__file__)))))    # ../../../../

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '78x!t-jmbhz*sbl67m!n2r1xh4*b#-)d%55h)hx=u32uhnj9wy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
CSRF_COOKIE_SECURE = False
ALLOWED_HOSTS = ['*']

ETH0_ADDR = None
if 'en0' in ni.interfaces():
    ETH0_ADDR = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
if 'eth0' in ni.interfaces():
    ETH0_ADDR = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

# Application definition

INSTALLED_APPS = [
    # Django admin
    'grappelli',
    'django.contrib.admin',

    # Django
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party
    'taggit',
    'tinymce',
    'storages',
    'imagekit',
    'django_extensions',

    # local apps
    'core',
    'post',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ads.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            pjoin(APP_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'ads.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Configures manually
ENVIRONMENT = 'local'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#
STATICFILES_DIRS = (
    pjoin(APP_DIR, 'static'),
)

MEDIA_ROOT = pjoin(APP_DIR, 'assets', 'media')
STATIC_ROOT = os.path.join(APP_DIR, 'assets', 'static')

MEDIA_URL = '/assets/media/'
STATIC_URL = '/assets/static/'

# django-imagekig
#
# https://django-imagekit.readthedocs.io/en/latest/configuration.html
#
#  IMAGEKIT_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'

# tinymce
#
# https://django-tinymce.readthedocs.io/en/latest/search.html?q=TINYMCE_DEFAULT_CONFIG&check_keywords=yes&area=default
#
TINYMCE_JS_URL = 'https://cdn.tinymce.com/4/tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'height': 756,
    'width': 980,

    'body_class': 'container',
    'content_css': '/assets/static/css/app.min.css',

    'selector': 'textarea',
    'language': 'ja',

    'mode': "exact",
    'theme': "modern",

    'autosave_interval': "60s",
    'visual': True,
    'menubar': True,
    'statusbar': True,

    'verify_html': False,
    'inline_styles': True,
    'valid_elements': 'a[href|target=_blank],strong/b,div[align],br',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'paste_as_text': False,

    'toolbar1': '''
    restoredraft undo redo | formatselect | bold italic underline strikethrough | blockquote bullist numlist hr
    | link unlink | table | imageupload image media | forecolor backcolor removeformat
    | alignleft aligncenter alignright indent outdent | fullscreen | code
    ''',

    'plugins': '''
    link image lists hr
    code fullscreen media imageupload
    table contextmenu textcolor autolink paste autosave save
    ''',

    'font_formats': 'Arial=arial,helvetica,sans-serif;Courier New=courier new,courier,monospace;AkrutiKndPadmini=Akpdmi-n',
    'fontsize_formats': '6pt 8pt 10pt 12pt 14pt 18pt 24pt 36pt',

    'style_formats_merge': True,
    'style_formats': [{
        'title': "Margin", 'items': [
            {'title': "10", 'selector': 'div', 'styles': {'margin': '10px'}},
            {'title': "20", 'selector': 'div', 'styles': {'margin': '20px'}},
            {'title': "30", 'selector': 'div', 'styles': {'margin': '30px'}},
            {'title': "40", 'selector': 'div', 'styles': {'margin': '40px'}},
            {'title': "50", 'selector': 'div', 'styles': {'margin': '50px'}},
            {'title': "60", 'selector': 'div', 'styles': {'margin': '60px'}},
            {'title': "70", 'selector': 'div', 'styles': {'margin': '70px'}},
            {'title': "80", 'selector': 'div', 'styles': {'margin': '80px'}},
            {'title': "90", 'selector': 'div', 'styles': {'margin': '90px'}},
        ]
    }, {
        'title': "Padding", 'items': [
            {'title': "10", 'selector': 'div', 'styles': {'padding': '10px'}},
            {'title': "20", 'selector': 'div', 'styles': {'padding': '20px'}},
            {'title': "30", 'selector': 'div', 'styles': {'padding': '30px'}},
            {'title': "40", 'selector': 'div', 'styles': {'padding': '40px'}},
            {'title': "50", 'selector': 'div', 'styles': {'padding': '50px'}},
            {'title': "60", 'selector': 'div', 'styles': {'padding': '60px'}},
            {'title': "70", 'selector': 'div', 'styles': {'padding': '70px'}},
            {'title': "80", 'selector': 'div', 'styles': {'padding': '80px'}},
            {'title': "90", 'selector': 'div', 'styles': {'padding': '90px'}},
        ]
    }],

    'image_advtab': True,
    'relative_urls': False,
    'remove_script_host': False,
}


TINYMCE_EXTRA_MEDIA = {
    'css': {
        'all': [
            'css/vendor.min.css',
            'css/app.min.css',
        ],
    },
    'js': [
        'js/prepared.min.js',
        'js/vendor.min.js',
        'js/app.min.js',
    ],
}


# Logging
#
LOGGING_PREFIX = 'ads'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': ('%(log_color)s[%(levelname)s]'
                       '[in %(pathname)s:%(lineno)d]'
                       '%(asctime)s %(process)d %(thread)d '
                       '%(module)s: %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'bold_black',
                'INFO': 'white',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
        'sql': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(cyan)s[SQL] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'syslog_verbose': {
            'format': ('{}:[%(levelname)s] [in %(pathname)s:%(lineno)d] '
                       '%(asctime)s %(process)d %(thread)d '
                       '%(module)s: %(message)s'.format(LOGGING_PREFIX)),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # 'sentry': {
        #     'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        #     'tags': {'environment': ENVIRONMENT},
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'raven': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        LOGGING_PREFIX: {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

