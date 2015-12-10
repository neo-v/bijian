"""
__author__ = 'Neo'
extend mixins to return json data with error code field
format
{
    error_code:
    data:
}

"""
from __future__ import unicode_literals
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from login.errorcode import SUCCESS
import logging

logger = logging.getLogger(__name__)


def make_response(response):
    """
    return format response data

    """
    data = {"error_code": SUCCESS}

    if isinstance(response.data, list):
        # logger.debug('make_response:' + str(response.data))
        for i, item in enumerate(response.data):
            response.data[i] = dict(item)

    data["data"] = response.data
    response.data = data
    logger.debug('make_response:' + str(response.data))

    return response


class JsonCreateMixin(CreateModelMixin):
    """
    create a object
    override create method
    return whth error_code:success
    """
    def create(self, request, *args, **kwargs):
        response = super(JsonCreateMixin, self).create(request, *args, **kwargs)
        logger.debug('JsonCreateMixin:create:' + str(type(response.data)))

        return make_response(response)


class JsonListMixin(ListModelMixin):
    """
    List a queryset.
    override list method
    return whth error_code:success
    """
    def list(self, request, *args, **kwargs):
        response = super(JsonListMixin, self).list(request, *args, **kwargs)
        logger.debug('JsonListMixin:list:' + str(type(response.data)))

        return make_response(response)


class JsonRetrieveMixin(RetrieveModelMixin):
    """
    Retrieve a model instance.
    override retrieve method
    return whth error_code:success
    """
    def retrieve(self, request, *args, **kwargs):
        response = super(JsonRetrieveMixin, self).retrieve(request, *args, **kwargs)
        logger.debug('JsonRetrieveMixin:retrieve:' + str(type(response.data)))

        return make_response(response)


class JsonUpdateMixin(UpdateModelMixin):
    """
    Update a model instance.
    override update method
    return whth error_code:success
    """
    def update(self, request, *args, **kwargs):
        response = super(JsonUpdateMixin, self).update(request, *args, **kwargs)
        logger.debug('JsonUpdateMixin:update:' + str(type(response.data)))
        return make_response(response)


class JsonDestroyMixin(DestroyModelMixin):
    """
    Destroy a model instance.
    override destroy method
    return whth error_code:success
    """
    def destroy(self, request, *args, **kwargs):
        response = super(JsonDestroyMixin, self).destroy(request, *args, **kwargs)
        logger.debug('JsonDestroyMixin:destroy:' + str(type(response.data)))
        return make_response(response)
