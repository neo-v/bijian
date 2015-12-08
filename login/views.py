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

from login.serializers import ParentSerializer
from login.serializers import ClassInfoSerializer
from login.serializers import TeacherSerializer
from login.serializers import CourseInfoSerializer
from login.serializers import SchoolSerializer
from login.serializers import OrganizationSerializer
from login.serializers import CreateUserSerializer

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import exceptions

from login.exceptions import KeyFoundError, NotLogin
from login import errorcode
from django.core.exceptions import ValidationError
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


class ParentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be register as parents
    fill with detail information

    """
    permission_classes = (IsAuthenticated,)
    queryset = ParentDetail.objects.all()
    serializer_class = ParentSerializer
    # lookup_field = 'user_id'


class TeacherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be register as a Teacher
    fill with detail information

    """
    permission_classes = (IsAuthenticated,)
    queryset = TeacherDetail.objects.all()
    serializer_class = TeacherSerializer
    # lookup_field = 'user_id'


class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be register as School

    """
    permission_classes = (IsAuthenticated,)
    queryset = SchoolDetail.objects.all()
    serializer_class = SchoolSerializer


class OrganiztionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be register as a Organization

    """
    permission_classes = (IsAuthenticated,)
    queryset = OrganizationDetail.objects.all()
    serializer_class = OrganizationSerializer


class ClassInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that list all class information

    """
    permission_classes = (IsAuthenticated,)
    queryset = ClassInformation.objects.all()
    serializer_class = ClassInfoSerializer


class CourseInfoViewSet(viewsets.ModelViewSet):
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
        'teachers': reverse('teacherdetail-list', request=request),
        'schools': reverse('schooldetail-list', request=request),
        'organizations': reverse('organizationdetail-list', request=request),
        'classinfomation': reverse('classinfo-list', request=request),
        'courseinfomation': reverse('courseinfo-list', request=request)
    })
