"""
__author__ = 'Neo'
Custom handled exceptions raised by REST framework.
"""

from rest_framework.views import exception_handler
from login.errorcode import get_errorcode
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from login import errorcode
import logging

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    logger.debug('api exception handler enter:' + exc.__class__.__name__)
    # Now add the error code to the response.
    if response and 'detail' not in response.data:
        logger.debug('api exception handler:reponse: ' + str(response.data))
        data = str(response.data)
        response.data.clear()
        response.data['detail'] = data

    if response is not None:
        response.data['error_code'] = get_errorcode(exc)

    logger.debug('api exception handler leave:')
    return response


class KeyFoundError(APIException):
    """
    Key error from request data
    """
    error_code = errorcode.KEYNOTFOUND
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('"{key}" do not found in request data ')

    def __init__(self, key, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail).format(key=key)


class NotLogin(APIException):
    """
    not login yet
    """
    error_code = errorcode.NOTLOGINYET
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('not login yet')
