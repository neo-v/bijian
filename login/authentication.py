"""
__author__ = 'Neo'
custom auth backend
auth by username or email
"""

from login.models import LocalUser
from rest_framework import authentication
from rest_framework import exceptions
from django.db.models import Q
from login import errorcode
import logging
from login.serializers import AuthUserSerializer


# get logger
logger = logging.getLogger(__name__)


class LocalUserAuthentication(authentication.BaseAuthentication):
    """
    args:username could be username , telephone or email
    """
    serializer = AuthUserSerializer

    def authenticate(self, request):
        logger.debug('get LocalUserAuthentication method:authenticate')
        se = self.serializer(data=request.data)
        try:
            se.is_valid(raise_exception=True)
            username = se.data['username']
            password = se.data['password']
        except KeyError:
            logger.debug('get LocalUserAuthentication method:authenticate:KeyError:' + str(se.data))
            return None
        except exceptions.ValidationError, e:
            logger.debug('get LocalUserAuthentication method:authenticate:ValidationError' + e.__str__())
            return None

        if not username or not password:
            logger.debug('get LocalUserAuthentication method:authenticate:empty')
            exc = exceptions.AuthenticationFailed('credentials is empty')
            setattr(exc, 'error_code', errorcode.KEYNOTFOUND)
            raise exc

        try:
            user = LocalUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                logger.debug('get LocalUserAuthentication method:authenticate:ok')
                return user, None
        except LocalUser.DoesNotExist:
            logger.debug('get LocalUserAuthentication method:authenticate:notExist')
            exc = exceptions.AuthenticationFailed()
            setattr(exc, 'error_code', errorcode.LOGNGERROR)
            raise exc


