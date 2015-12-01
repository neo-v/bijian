"""
__author__ = 'Neo'
Custom handled exceptions raised by REST framework.
"""

from rest_framework.views import exception_handler
from login.errorcode import get_errorcode
from rest_framework.exceptions import APIException


def api_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the error code to the response.
    if response is not None:
        response.data['error_code'] = get_errorcode(exc)

    return response


class ExtendException(APIException):
    """
    Some other error
    """