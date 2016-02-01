# -*- coding: utf-8 -*-
"""
Django settings for estavos project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# For bootstrap css
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q%ug)v2h!4-l6(=9195*u=+qwvwd+cxc+e^qom6_3!+)e=&_3k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', ]


# Application definition

INSTALLED_APPS = (
    'flat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'utils',
    'tinymce',
    'portal',
    'galeria',
    'partner',
    'core',
    'esap',
    'account',
    'django_summernote',
    'django_forms_bootstrap',
    'captcha',
    'course',
    'pagseguro',
    'tournament',
    'jquery_ui',
    'import_export',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.current_user.CurrentUserMiddleware',
)

ROOT_URLCONF = 'estavos.urls'

WSGI_APPLICATION = 'estavos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt_BR'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = "."
DECIMAL_SEPARATOR = ","
NUMBER_GROUPING = 3

MESSAGE_TAGS = {message_constants.ERROR: "danger"}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Admins for Django report error
ADMINS = (('Bruno Barbosa', 'bsbruno1@gmail.com'), )


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'


# TinyMCE setup
TINYMCE_JS_URL = os.path.join(STATIC_URL, "site/js/tinymce/tinymce.min.js")
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'site/js/tinymce/')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "modern",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
}

# Template dirs
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'portal.context_processors.all_pages',
    'esap.context_processors.dashboard',
    'esap.context_processors.menu',
)

# Email
# https://docs.djangoproject.com/en/1.7/topics/email/#configuring-email-for-development
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# Authentication
AUTH_USER_MODEL = 'account.User'

# File system storage - fix ascii errors on filename
DEFAULT_FILE_STORAGE = 'utils.asciifilesystemstorage.ASCIIFileSystemStorage'

# Django reCAPTCHA
RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True
RECAPTCHA_USE_SSL = True


DATE_INPUT_FORMATS = (
    "%d/%m/%Y", "%d/%m/%y"
)

# PAGSEGURO SETUP
PAGSEGURO_EMAIL = ''
PAGSEGURO_TOKEN = ''
PAGSEGURO_SANDBOX = True  # se o valor for True, as requisições a api serão feitas usando o PagSeguro Sandbox.
PAGSEGURO_LOG_IN_MODEL = True  # se o valor for True, os checkouts e transações vão ser logadas no database.
