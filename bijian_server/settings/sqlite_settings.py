"""
settings used for sqlite
"""
from BaseSettings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
     }
}

AUTH_USER_MODEL = 'login.LocalUser'
LOGIN_REDIRECT_URL = '/api'
