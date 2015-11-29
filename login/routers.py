"""
__author__ = 'Neo'
custom routers
"""

from rest_framework.routers import Route, SimpleRouter


class RegiserRouter(SimpleRouter):
    """
    A router for register
    """
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'post': 'create', 'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'retrieve', 'put': 'update'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
    ]


class ReadOnlyRouter(SimpleRouter):
    """
    A router for read only information
    """
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'retrieve', },
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
    ]
