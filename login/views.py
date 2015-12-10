"""
login views
author :Neo
"""
from login.models import LocalUser
from login.models import TeacherDetail
from login.models import ParentDetail
from login.models import SchoolDetail
from login.models import OrganizationDetail
from login.models import ClassInformation
from login.models import CourseInformation

from rest_framework import viewsets

from login.serializers import FullParentSerializer, BasicParentSerializer
from login.serializers import ClassInfoSerializer
from login.serializers import FullTeacherSerializer, BasicTeacherSerializer
from login.serializers import CourseInfoSerializer
from login.serializers import FullSchoolSerializer, BasicSchoolSerializer
from login.serializers import FullOrganizationSerializer, BasicOrganizationSerializer
from login.serializers import CreateUserSerializer
from login.view_mixins import JsonCreateMixin, JsonListMixin, JsonRetrieveMixin, JsonUpdateMixin, JsonDestroyMixin


from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.viewsets import GenericViewSet

from login.exceptions import KeyFoundError, NotLogin
from login import errorcode
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.http import Http404
import logging

# get logger
logger = logging.getLogger(__name__)


def make_success_data(data={}):
    """
    add error code
    """
    data['error_code'] = errorcode.SUCCESS
    # logger.debug('make_success_data: ' + str(data))
    return data


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    """
    Same as Django's standard shortcut, but make sure to also raise 404
    if the filter_kwargs don't match the required types.
    """
    try:
        logger.debug('get_object_or_404')
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except (TypeError, ValueError, Http404), e:
        logger.debug('get_object_or_404:except:' + e.__str__())
        raise exceptions.NotFound()


class JsonModelViewSet(JsonCreateMixin, JsonListMixin, JsonRetrieveMixin,
                       JsonUpdateMixin, JsonDestroyMixin, GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    return with error code ,default value: SUCCESS
    """
    pass


# Create your views here.
class UserInfoView(APIView):
    """
    user view for register,get and edit profile

    method get, post ,put
    """

    def post(self, request):
        """
        user view for register
        """
        logger.debug('get userinfoview method:post')
        se = CreateUserSerializer(data=request.data)
        try:
            se.is_valid(raise_exception=True)
            tel = se.data['telephone']
            password = se.data['password']
            status = se.data['status']
        except KeyError, e:
            logger.debug('get userinfoview method:post:keyError:' + str(se.data))
            raise KeyFoundError(e.__str__())
        except exceptions.ValidationError, e:
            logger.debug('get userinfoview method:post:ValidationError' + e.__str__())
            raise e

        user = LocalUser(telephone=tel, status=status)
        user.set_password(password)
        user.save()

        return Response(make_success_data())

    def get(self, request):
        """
        get user profile
        """
        logger.info('get userinfoview method:get')
        if request.user.is_authenticated():
            reg_info = LocalUser.objects.filter(telephone=request.user.get_username()).values('telephone',
                                                                                              'username',
                                                                                              'email',
                                                                                              'status',
                                                                                              'date_joined')
            logger.debug('get userinfoview method:get:reg_info: ' + str(reg_info))
            return Response(make_success_data(reg_info[0]))
        else:
            logger.debug('get userinfoview method:get:notLogin')
            raise NotLogin()

    def put(self, request):
        """
        update user reg profile
        """
        logger.debug('get userinfoview method:put')

        if request.user.is_authenticated():
            if hasattr(request.data, 'password'):
                logger.debug('get userinfoview method:put:setpassword')
                request.user.set_password(getattr(request.data, 'password'))
                request.data.pop('password')

            # unique check for telephone,username,email
            for attr, value in request.date.items():
                setattr(request.user, attr, value)
            try:
                request.user.full_clean()
                request.user.save()
            except ValidationError as e:
                logger.debug('get userinfoview method:put:validationError')

                exc = serializers.ValidationError()
                if 'telephone' in e.message_dict:
                    setattr(exc, 'error_code', errorcode.TELEPHONE_EXISTS)
                    exc.detail = e.message_dict['telephone']

                elif 'username' in e.message_dict:
                    setattr(exc, 'error_code', errorcode.USERNAME_EXISTS)
                    exc.detail = e.message_dict['username']

                elif 'email' in e.message_dict:
                    setattr(exc, 'error_code', errorcode.EMAIL_EXISTS)
                    exc.detail = e.message_dict['email']

                raise exc

            return Response(make_success_data())
        else:
            logger.debug('get userinfoview method:put:notLogin')
            raise NotLogin()


class DetailView(JsonModelViewSet):
    """
    Base class for detail viewset
    override get_obj()
    voerride get_serializer()

    """
    permission_classes = (IsAuthenticated,)
    lookup_field = 'user_id'

    def get_object(self):
        """
        Returns the object the view is displaying.
        override return auth user-detail object
        """
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        if self.request.method == 'PUT':
            filter_value = str(self.request.user.pk)
        else:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )
            filter_value = self.kwargs[lookup_url_kwarg]

        logger.debug(self.__class__.__name__ + ':get_object:filter_value:' + filter_value)

        filter_kwargs = {self.lookup_field: filter_value}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        """
        Return the class to use for the serializer for diff user
        Defaults to using `self.serializer_class`.

        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        try:
            if self.request.method == 'GET' and (self.kwargs[lookup_url_kwarg] == str(self.request.user.id)):
                logger.debug(self.__class__.__name__ + ':get_serializer_class:owner')
                return self.full_serializer_class
        except KeyError, e:
            logger.debug(self.__class__.__name__ + ':get_serializer_class:keyError:' + e.__str__())
        logger.debug(self.__class__.__name__ + ':get_serializer_class:others:')
        return self.basic_serializer_class


class ParentViewSet(DetailView):
    """
    API endpoint that allows user to be register as parents
    fill with detail information

    """
    queryset = ParentDetail.objects.all()
    full_serializer_class = FullParentSerializer
    basic_serializer_class = BasicParentSerializer


class TeacherViewSet(DetailView):
    """
    API endpoint that allows user to be register as a Teacher
    fill with detail information

    """
    queryset = TeacherDetail.objects.all()
    full_serializer_class = FullTeacherSerializer
    basic_serializer_class = BasicTeacherSerializer


class SchoolViewSet(DetailView):
    """
    API endpoint that allows user to be register as School

    """
    queryset = SchoolDetail.objects.all()
    full_serializer_class = FullSchoolSerializer
    basic_serializer_class = BasicSchoolSerializer


class OrganiztionViewSet(DetailView):
    """
    API endpoint that allows user to be register as a Organization

    """
    queryset = OrganizationDetail.objects.all()
    full_serializer_class = FullOrganizationSerializer
    basic_serializer_class = BasicOrganizationSerializer


class ClassInfoViewSet(JsonModelViewSet):
    """
    API endpoint that list all class information

    """
    permission_classes = (IsAuthenticated,)
    queryset = ClassInformation.objects.all()
    serializer_class = ClassInfoSerializer


class CourseInfoViewSet(JsonModelViewSet):
    """
    API endpoint that list all course information

    """
    permission_classes = (IsAuthenticated,)
    queryset = CourseInformation.objects.all()
    serializer_class = CourseInfoSerializer


@api_view(('GET',))
# @permission_classes([IsAuthenticated],)
def api_root(request):
    """
    API entry point
    param request:get
    """

    return Response({
        'users': reverse('localuser-list', request=request),
        'parents': reverse('parentdetail-list', request=request),
        'parents/id': reverse('parentdetail-detail', request=request, kwargs={"user_id": 1}),
        'teachers': reverse('teacherdetail-list', request=request),
        'teachers/id': reverse('teacherdetail-detail', request=request, kwargs={"user_id": 1}),
        'schools': reverse('schooldetail-list', request=request),
        'schools/id': reverse('schooldetail-detail', request=request, kwargs={"user_id": 1}),
        'organizations': reverse('organizationdetail-list', request=request),
        'classinfomation': reverse('classinfo-list', request=request),
        'courseinfomation': reverse('courseinfo-list', request=request)
    })
