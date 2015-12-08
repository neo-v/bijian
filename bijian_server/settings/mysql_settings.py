"""
settings used for mysql
"""
from BaseSettings import *


DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bijian_sql_db',
        'USER': 'kumeng_1234',
        'PASSWORD': 'kumeng_1234',
        'HOST': 'rds6iby5sh94840g8e06.mysql.rds.aliyuncs.com',
        'PORT': '3306',
   }
}

AUTH_USER_MODEL = 'login.LocalUser'
