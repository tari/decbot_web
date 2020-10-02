"""
Django settings for decbot_web project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xgu9r*2+5yyo@-07&m-n2ue(0s*+^fzfgGmz4k^d,(^33)(jaa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['.cemetech.net']


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'quotes',
    'karma'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

# Make things slow.
#    'decbot_web.middleware.SlowPony',
)

ROOT_URLCONF = 'decbot_web.urls'

WSGI_APPLICATION = 'decbot_web.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'merthsoft',
        'USER': 'merthsoft',
        'PASSWORD': 'whyxcE2vBhcAmxrX',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = '/home/tari/projects/decbot_web/static_root/'

# I'm not sure why this is here. It's been here since I last touched the
# code, so who knows if it does anything useful.
#STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
#PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.closure.ClosureCompressor'
#PIPELINE_CLOSURE_ARGUMENTS = '--language_in ECMASCRIPT5_STRICT'
#PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.csstidy.CSSTidyCompressor'
#
#PIPELINE_CSS = {
#    'ns': {
#        'source_filenames': ('css/main.css', 'css/ns.css'),
#        'output_filename': 'css/ns.css',
#    },
#    'angular': {
#        'source_filenames': ('css/main.css', 'css/angular.css'),
#        'output_filename': 'css/angular.css',
#    }
#}
#PIPELINE_JS = {
#    'libs': {
#        'source_filenames': ('lib/*.js',),
#        'output_filename': 'js/libs.js',
#    },
#    'decbot': {
#        'source_filenames': ('app/*.js',),
#        'output_filename': 'js/decbot.js',
#    }
#}

STATIC_ROOT = '/home/tari/decbot.cemetech.net/public_html/static/'

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'PAGINATE_BY': 50,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}
