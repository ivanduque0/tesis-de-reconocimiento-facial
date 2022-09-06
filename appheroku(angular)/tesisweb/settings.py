"""
Django settings for tesisweb project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from ctypes import cast
from pathlib import Path
import os
import cloudinary
import cloudinary_storage
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default='foo')
#SECRET_KEY = 'django-insecure-&8obmcszqc!6!#6-u_=y7o0rj48=wc8@v5@p9v9)mrg@-h#$7@'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = int(os.environ.get("DEBUG", default=0))
# DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG = False

#ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = ['tesis-reconocimiento-facial.herokuapp.com', ]


# Application definition

INSTALLED_APPS = [
    'web',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tesisweb.urls'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://tesis-reconocimiento-facial.herokuapp.com/',
    'https://tesis-reconocimiento-facial.herokuapp.com/',

)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
'Access-Control-Allow-Origin',)

ROOT_URLCONF = 'tesisweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tesisweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
#         'NAME': os.environ.get("SQL_DATABASE",  BASE_DIR / "db.sqlite3"),
#         'USER': os.environ.get("SQL_USER", "user"),
#         'PASSWORD': os.environ.get("SQL_PASSWORD", "password"),
#         'HOST': os.environ.get("SQL_HOST", "locahost"),
#         'PORT': os.environ.get("SQL_PORT", "5432"),
#     }
# }

import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)


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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-VE'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME', default=""),
    'API_KEY': config('API_KEY', default=""),
    'API_SECRET': config('API_SECRET', default=""),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
    )
}

CSRF_TRUSTED_ORIGINS = ['https://tesis-reconocimiento-facial.herokuapp.com','http://tesis-reconocimiento-facial.herokuapp.com']

# CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ")

AUTH_USER_MODEL = 'web.User'

CSRF_COOKIE_HTTPONLY = False  # False since we will grab it via universal-cookies
SESSION_COOKIE_HTTPONLY = False