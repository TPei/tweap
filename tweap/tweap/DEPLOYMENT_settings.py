"""
Django settings for tweap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from easy_thumbnails.conf import Settings as ThumbnailSettings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3gtff-keg7%50ieg1kf(#k$^g*8bgh^kwq43vavkzon^#5dm1r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
#TODO: ja, hier muss irgendwie der lokale Pfad vom Server stehen

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_management',
    'project_management',
    'rosetta',
    'image_cropping',
    'easy_thumbnails',
    'dashboard',
    'settings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tweap.middleware.RequireLoginMiddleware',
)

ROOT_URLCONF = 'tweap.urls'

WSGI_APPLICATION = 'tweap.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'tweap',
        'USER': 'root',
        'PASSWORD': 'tweap',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR + "/tweap/", 'static'),
)

STATIC_ROOT = "/home/goggelz/STATIC_DJANGO/tweap/"

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR + "/tweap/",  'templates'),
)

# non standard values

LOGIN_REDIRECT_URL = 'dashboard:home'

LOGIN_URL = 'user_management:login'

LOGIN_REQUIRED_URLS = (
    r'/projects/(.*)$',
    r'/users/profile/(.*)$',
    r'/users/editprofile/$',
    r'/settings/$',
)

LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/users/login$',
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ("en", "English"),
    ("de", "Deutsch"),
    ("pl", "Polski"),
)

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + ThumbnailSettings.THUMBNAIL_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.contrib.auth.context_processors.auth",
    "user_management.context_processors.user_info"
)
