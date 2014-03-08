# coding: utf-8

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

DATE_FORMAT = 'd.m.Y'

DEBUG = True

DECIMAL_SEPARATOR = ','

INSTALLED_APPS = (
    'statements',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
)

LANGUAGE_CODE = 'fr'

ROOT_URLCONF = 'lcl.urls'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

STATIC_URL = '/static/'

TIME_ZONE = 'Europe/Paris'

WSGI_APPLICATION = 'lcl.wsgi.application'
