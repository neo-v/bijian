"""
settings used for mysql
"""
from BaseSetting import *


DATABASES = {
   'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_1234',
        'USER': 'test_1234',
        'PASSWORD': '123456',
        'HOST': 'rdsv063y063k4cv6jkf3.mysql.rds.aliyuncs.com',
        'PORT': '3306',
   }
}

AUTH_USER_MODEL = 'login.LocalUser'
