"""
"__author__ = 'Neo'
Descriptive Error codes, for code readability.

"""

# OK
SUCCESS = 0

# user auth error

TELEPHONE_EXISTS = 1000


def get_errorcode(exc):
    """
    get error code according to exceptions

    """
    if hasattr(exc, 'error_code'):
        return exc.error_code
    else:
        return exc.status_code




