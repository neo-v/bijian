"""
settings used for mysql
"""
from BaseSettings import *


DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bijian_sql_db',
        'USER': 'kumeng_1234',
        'PASSWORD': 'kumeng1234',
        'HOST': 'rdsaliyunbijiansql1234.mysql.rds.aliyuncs.com',
        'PORT': '3306',
   }
}

AUTH_USER_MODEL = 'login.LocalUser'
