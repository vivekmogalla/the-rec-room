"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import sys
import dj_database_url

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

####################
# Secret key in the development is different to the production secret key
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = os.getenv('DEBUG', 'False') == 'True'
# DEBUG = True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(",")
# ALLOWED_HOSTS=['localhost', '127.0.0.1']

WEBSITE_URL = os.getenv('DJANGO_WEBSITE_URL', 'http://127.0.0.1:8000')
# WEBSITE_URL = 'http://127.0.0.1:8000'

DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', False) == True

USE_SPACES = os.getenv('USE_SPACES', True) == True

AUTH_USER_MODEL = 'account.User'
################################


# Email configuration
############################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'therecroom.development@gmail.com'
EMAIL_HOST_PASSWORD = 'gbqsupzrnzyuulfq' # Note that this should be the App password rather than your Google account password
EMAIL_PORT = 465
EMAIL_USE_SSL = True
##############################

# Application definition

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=180),
    'ROTATE_REFRESH_TOKEN': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'https://the-rec-room.vercel.app',
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'https://the-rec-room.vercel.app',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'account',
    'post',
    'search',
    'chat',
    'notification',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEVELOPMENT_MODE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# DigitalOcean Spaces configuration (static + media files)
# https://blog.devgenius.io/django-digitalocean-spaces-a12b4a053628

USE_SPACES = os.getenv('USE_SPACES')
if USE_SPACES:
    # settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # static settings
    AWS_LOCATION = os.environ.get("AWS_LOCATION")
    # STATICFILES_STORAGE setting configures django to automatically add static files
    # to the spaces bucket when the collect static command is run
    STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE")
    # media settings
    AWS_MEDIA_LOCATION = 'media'
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_MEDIA_LOCATION}/'
    # DEPRECATED:
    DEFAULT_FILE_STORAGE = 'backend.storage_backend.MediaStorage'
    # STORAGES = {
    #     'staticfiles': {
    #         'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    #     },
    #     'default': {
    #         'BACKEND': 'backend.storage_backend.MediaStorage',
    #     },
    # }
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


####################
# In production, we want cdn - STATIC_ROOT  = BASE_DIR/ 'staticfiles-cdn' # In production, we want cdn

# https://www.cfe.sh/blog/django-static-files-digitalocean-spaces

# https://djangostoragew.blr1.digitaloceanspaces.com

# bucket name is djangostoragew

# origin Endpoint - https://djangostoragew.blr1.digitaloceanspaces.com
###################

# STATICFILES_DIRS = os.path.join(BASE_DIR, 'rec-room-media/static')
#
# STATICFILES_DIRS = (
#     # os.path.join(BASE_DIR, 'static'),
#     os.path.join(BASE_DIR, ),
# )
# MEDIAFILES_DIRS = (
#     os.path.join(BASE_DIR, 'media')
# )

###########
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
#     os.path.join(BASE_DIR, 'media/static'),
# ]
# MEDIAFILES_DIRS = [
#     os.path.join(BASE_DIR, 'media')
# ]
##########

# AWS_ACCESS_KEY_ID = 'key_id'
# AWS_SECRET_ACCESS_KEY = 'access_key'
# AWS_STORAGE_BUCKET_NAME = 'bucket_name'
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com' # Make sure nyc3 is correct
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400'
# }

# AWS_STATIC_LOCATION = 'static'
# STATIC_URL = '%s/%s' % (AWS_S3_ENDPOINT_URL, AWS_STATIC_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_MEDIA_LOCATION = 'media'
# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = '%s%s' % (AWS_S3_ENDPOINT_URL, AWS_MEDIA_LOCATION)
# DEFAULT_FILE_STORAGE = 'backend.storage_backend.MediaStorage'
# DEFAULT_FILE_STORAGE = 'storage_backend.MediaStorage'


##########

    # AWS_ACCESS_KEY_ID = 'DO00DAL3UK9MFXVY8Q37'
    # AWS_SECRET_ACCESS_KEY = 'rMelz75sMbtVcfyH0DRJXAPWcIdTMNi5u1p9DWr3jQk'
    # AWS_STORAGE_BUCKET_NAME = 'mediabucket'
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

##########

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/




# MEDIAFILES_DIRS = [
#     os.path.join(BASE_DIR, 'media')
# ]
from .cdn.conf import *
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

