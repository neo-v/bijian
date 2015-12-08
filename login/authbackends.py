"""
__author__ = 'Neo'
custom auth backend
auth by username or email
"""

from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
import logging
from django.contrib.auth import get_user_model


# get logger
logger = logging.getLogger(__name__)


class LocalUserAuthentication(ModelBackend):
    """
    args:username could be username , telephone or email
    """

    def authenticate(self, username=None, password=None, **kwargs):
        logger.debug('get LocalUserAuthentication method:authenticate')

        if username and password:
            LocalUser = get_user_model()
            try:
                user = LocalUser.objects.get(Q(username=username) | Q(email=username))
                if user.check_password(password):
                    logger.debug('get LocalUserAuthentication method:authenticate:ok')
                    return user
            except LocalUser.DoesNotExist:
                logger.debug('get LocalUserAuthentication method:authenticate:notExist')
                LocalUser().set_password(password)
                # return None

