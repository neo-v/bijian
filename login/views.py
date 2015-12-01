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

from login.serializers import UserSerializer
from login.serializers import ParentSerializer
from login.serializers import ClassInfoSerializer
from login.serializers import TeacherSerializer
from login.serializers import CourseInfoSerializer
from login.serializers import SchoolSerializer
from login.serializers import OrganizationSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated


# Create your views here.
# login and register in system,with json data
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user to be register

    """
    permission_classes = (IsAuthenticated,)
    queryset = LocalUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'telephone'


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
def api_root(request):
    """
    API entry point
    param request:get
    return:
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
