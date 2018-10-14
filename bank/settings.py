# coding: utf-8

import os

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

DATE_FORMAT = "d.m.Y"

DEBUG = True

DECIMAL_SEPARATOR = ","

INSTALLED_APPS = [
    "statements",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

LANGUAGE_CODE = "fr"

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "bank.middleware.AdminAutoLoginMiddleware",
]

ROOT_URLCONF = "bank.urls"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")

STATIC_URL = "/static/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

TIME_ZONE = "Europe/Paris"

WSGI_APPLICATION = "bank.wsgi.application"
