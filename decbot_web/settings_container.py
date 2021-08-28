import json
import os

from decbot_web.settings import *

def env_var(name, required=True, default=None):
    if required:
        return os.environ[name]
    else:
        return os.environ.get(name, default)

SECRET_KEY = env_var('DECBOT_WEB_SECRET_KEY')
DEBUG = env_var('DECBOT_WEB_DEBUG', required=False, default=False)

import pymysql
pymysql.install_as_MySQLdb()
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    # OPTIONS fills in keyword arguments to MySQLdb.connect(). Typical options
    # will include host, user, passwd, and db.
    'OPTIONS': json.loads(env_var('DATABASE_OPTIONS', required=False, default='{}'))
}

# Use whitenoise to serve static files direct through the WSGI server,
# efficiently.
MIDDLEWARE.insert(0, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
