"""
Django settings for plants_app project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import environ

import dj_database_url
import django_heroku
import cloudinary
import cloudinary_storage

from pathlib import Path

from celery.schedules import crontab
from django.contrib import messages, staticfiles
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # development
# DEBUG = False  # production

ADMINS = (
    ('admin',),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ["*"]  # Don't use it for production.
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com', '.ngrok.io']

CSRF_TRUSTED_ORIGINS = ['https://*.ngrok.io', 'https://*.127.0.0.1', 'https://*.herokuapp.com']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'dal',
    'dal_select2',
    'whitenoise.runserver_nostatic',  # above the built-in staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'django_filters',
    'import_export',
    'crispy_forms',
    'ckeditor',
    'sorl.thumbnail',
    'rest_framework',
    'guardian',
    'translation_manager',
    'rosetta',
    'webpush',
    'cloudinary',
    'cloudinary_storage',
    'django_celery_results',
    'django_celery_beat',
    'django_crontab',
    'captcha',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'main.apps.MainConfig',
    'authentication.apps.AuthenticationConfig',
    'control_panel.apps.ControlPanelConfig',
    'blog.apps.BlogConfig',
    'galleries.apps.GalleriesConfig',
]

# LocaleMiddleware: # this middleware should come after the SessionMiddleware because it needs to use the session data.
# It should also be placed before the CommonMiddleware because the CommonMiddleware needs the active language to resolve
# the URLs being requested.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add whitenoise exactly here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # add exactly here
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'plants_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.mode',  # light/dark mode on all pages
            ],
        },
    },
]

WSGI_APPLICATION = 'plants_app.wsgi.application'

# Postgres database:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT')
    }
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# Database for Docker:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('POSTGRES_NAME'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": env("VAPID_PUBLIC_KEY"),
    "VAPID_PRIVATE_KEY": env("VAPID_PRIVATE_KEY"),
    "VAPID_ADMIN_EMAIL": env("VAPID_ADMIN_EMAIL")
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('pl', _('Polish')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = [BASE_DIR / 'locale', ]

LANGUAGE_COOKIE_NAME = 'django_language'

LANGUAGE_SESSION_KEY = '_language'

# TRANSLATIONS_BASE_DIR = BASE_DIR

TRANSLATIONS_IGNORED_PATHS = ['env', ]

TRANSLATIONS_MAKE_BACKUPS = True

TRANSLATIONS_CLEAN_PO_AFTER_BACKUP = False

TRANSLATIONS_ADMIN_EXCLUDE_FIELDS = ['get_hint', 'locale_parent_dir', 'domain']

TRANSLATIONS_HINT_LANGUAGE = 'en'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'  # the URL location of static files located in STATIC_ROOT
MEDIA_URL = '/media/'


if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'main/static'), ]  # Tells Django where to look for static files in a Django project.
else:
    STATIC_ROOT = os.path.join(BASE_DIR,
                               'main/static')  # The absolute path to the directory where collectstatic will collect static files for deployment.

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# To reduce the size of the static files when they are served (more efficient)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TEMPLATE_LOADERS = 'django.template.loaders.filesystem.Loader'

# To serve files directly from their original locations
WHITENOISE_USE_FINDERS = True

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env("CLOUD_NAME"),
    'API_KEY': env("API_KEY"),
    'API_SECRET': env("API_SECRET"),
}

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'authentication.backends.EmailBackend'
)

AUTH_USER_MODEL = 'authentication.User'

SHELL_PLUS_PRINT_SQL = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

SITE_ID = 2  # 2 will be if we've changed (add new) the example.com to the local address.

LOGIN_URL = '/authentication'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

NEWSLETTER_THUMBNAIL = 'sorl-thumbnail'
NEWSLETTER_ROOT = BASE_DIR / 'main/templates'

# Gmail Sending Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587  # this is gmail's port
EMAIL_USE_TLS = True  # this encrypts our emails being sent


# CELERY SETTINGS:
# Used to point a message broker to Celery (default port for the Redis server is 6379).
CELERY_BROKER_URL = env("CELERY_BROKER_URL")

# Task sent to the Celery worker must be serialized as JSON before it is sent, worker only process the JSON format tasks
CELERY_ACCEPT_CONTENT = ['application/json']

# Ensures that processed tasks are in JSON format.
CELERY_TASK_SERIALIZER = 'json'

# Orders that the results of Celery tasks will be serialized in JSON format before sent back to the Celery client.
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Warsaw'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Stores tasks status in django database
# CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_RESULT_BACKEND = 'django-db'

# Celery Beat settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'send-notification': {
        'task': 'planst_app.tasks.send_notification',
        'schedule': crontab(hour='16', minute='30', day_of_week='4'),
    },
    'send-mail-to-client': {
        'task': 'planst_app.tasks.send_mail_task',
        'schedule': crontab(hour='22', minute='10', day_of_week='4')
    },
}

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

# Django messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY = env("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = env("RECAPTCHA_PRIVATE_KEY")

# Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    # 'APP': {
    #     'client_id': env("CLIENT_ID"),
    #     'secret': env("SECRET"),
    #     'key': ''
    #
    # },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Additional configuration settings
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Login method to use: the user logs in by entering their email (also possible: username or username_email).
ACCOUNT_EMAIL_REQUIRED = True  # The user is required to hand over an e-mail address when signing up.
ACCOUNT_USERNAME_REQUIRED = False  # The user is required to enter a username when signing up.
ACCOUNT_UNIQUE_EMAIL = True  # Enforce uniqueness of e-mail addresses.
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Determines the e-mail verification method during signup. Setting this to 'mandatory' requires ACCOUNT_EMAIL_REQUIRED = True.
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # Determines the expiration date of email confirmation mails-in days.
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True  # When signing up, let the user type in their password twice to avoid typos.

SOCIALACCOUNT_AUTO_SIGNUP = True  # Attempt to bypass the signup form by using fields (e.g. username, email) retrieved from the social account provider.
SOCIALACCOUNT_EMAIL_VERIFICATION = ACCOUNT_EMAIL_VERIFICATION
SOCIALACCOUNT_EMAIL_REQUIRED = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_LOGOUT_ON_GET = True

# To activate django-heroku
django_heroku.settings(locals())
