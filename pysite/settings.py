"""
Django settings for pysite project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

import environ


env = environ.Env(
    DEBUG=(bool, False)
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    ALLOWED_HOSTS = [
        'pythondiscord.local',
        'admin.pythondiscord.local',
        'api.pythondiscord.local',
        'staff.pythondiscord.local',
        'wiki.pythondiscord.local'
    ]
    SECRET_KEY = "+_x00w3e94##2-qm-v(5&-x_@*l3t9zlir1etu+7$@4%!it2##"
else:
    ALLOWED_HOSTS = [
        'pythondiscord.com',
        'admin.pythondiscord.com',
        'api.pythondiscord.com',
        'staff.pythondiscord.local',
        'wiki.pythondiscord.local'
    ]
    SECRET_KEY = env('SECRET_KEY')


# Application definition

INSTALLED_APPS = [
    'api',
    'home',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_hosts',
    'rest_framework',
    'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
]
ROOT_URLCONF = 'pysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pysite', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'django_hosts.templatetags.hosts_override',
            ],

            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pysite', 'static')]

# django-hosts
# https://django-hosts.readthedocs.io/en/latest/
ROOT_HOSTCONF = 'pysite.hosts'
DEFAULT_HOST = 'home'

if DEBUG:
    PARENT_HOST = 'pythondiscord.local:8000'
else:
    PARENT_HOST = 'pythondiscord.com'

# Django REST framework
# http://www.django-rest-framework.org
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Bot API settings
BOT_API_KEY = env('BOT_API_KEY')
