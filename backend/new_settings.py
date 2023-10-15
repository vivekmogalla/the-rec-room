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

####################
# Important configurations
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', None)
DEBUG = os.getenv('DEBUG', None)
ALLOWED_HOSTS = ['*']
WEBSITE_URL = os.getenv('DJANGO_WEBSITE_URL', None)
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', None)
USE_SPACES = os.getenv('USE_SPACES', None)
#######################################
# DEBUG = os.getenv('DEBUG', False) == True

# WEBSITE_URL = os.getenv('DJANGO_WEBSITE_URL', 'http://127.0.0.1:8000')

# 1 .Need to test how the environment variales are getting stored in the new_settings ffile
# DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', False) == True
# USE_SPACES = os.getenv('USE_SPACES', True) == True

# ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(",")
# WEBSITE_URL = 'http://127.0.0.1:8000'

AUTH_USER_MODEL = 'account.User'
################################


# Email configuration
############################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'therecroom.development@gmail.com'
EMAIL_HOST_PASSWORD = 'gbqsupzrnzyuulfq'  # Note that this should be the App password rather than your Google account password
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

if DEVELOPMENT_MODE == 'True':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    # Running on production App Engine, so connect to Google Cloud SQL using //cloudsql/connection_name
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'HOST': 'db-postgresql-blr1-33262-do-user-14809034-0.b.db.ondigitalocean.com',
            'NAME': 'defaultdb',  # Replace it with actual database name
            'USER': 'doadmin',  # Replace it with  actual database user
            'PASSWORD': os.environ.get("DJANGO_DB_PASSWORD", None),  # Replace it with actual database password
            'PORT': 25060,  # Leave this empty
        }
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
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_LOCATION = os.environ.get("AWS_LOCATION")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # static settings
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'staticfiles')
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'mediafiles')
    # STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE")
    # DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

####################


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
