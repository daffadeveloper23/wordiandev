"""
Django settings for wordian_project project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--qae2d*o9-y(5@b@ggmf!%j3l!6r()5n(objb7r@)t!1)k9tn7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '.now.sh', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wordian',
    'tinymce',
    'whitenoise.runserver_nostatic',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'wordian_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wordian_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'railway',
       'USER': 'postgres',
       'PASSWORD': '61a5352AE4a*FCD-D14fCCFD3ca*Be1D',
       'HOST': 'monorail.proxy.rlwy.net',
       'PORT': '51424',
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

# TinyMCE
TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/a2z2b2vh998fxc5effkk7udpc9d4rfsj1gkpcc92h4wajpgq/tinymce/6/tinymce.min.js'
TINYMCE_COMPRESSOR = False

# Emailing Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'wordiandevelopment@gmail.com'
EMAIL_HOST_USER = 'wordiandevelopment@gmail.com'
EMAIL_HOST_PASSWORD = 'ohsdbdxsdchpwnwq'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 14400

AWS_ACCESS_KEY_ID = 'AKIAZI3BZN2VAKJPJN5L'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'wordiandev'
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = 'ap-southeast-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

#CSRF_TRUSTED_ORIGINS = ['https://4afa-110-137-194-125.ngrok-free.app']