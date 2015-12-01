"""
restful api design
use hyper linked model serializer
__author__ = 'Neo'

"""
from login.models import ClassInformation
from login.models import CourseInformation
from login.models import LocalUser
from login.models import ParentDetail
from login.models import TeacherDetail
from login.models import OrganizationDetail
from login.models import SchoolDetail

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = LocalUser
        fields = ('url', 'telephone', 'password', 'type', 'date_joined',)
        extra_kwargs = {
            'url': {'lookup_field': 'telephone'},
        }

    def create(self, validated_data):
        user = LocalUser(
            telephone=validated_data['telephone']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ParentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True,
                                               validators=[UniqueValidator(queryset=ParentDetail.objects.all())],
                                               view_name='localuser-detail',
                                               lookup_field='telephone')
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail')

    class Meta:
        model = ParentDetail
        # exclude = ('user', 'class_id')
        fields = '__all__'
        read_only_fields = ('id', 'user')


class TeacherSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='localuser-detail',
                                               lookup_field='telephone')
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail')
    course = serializers.HyperlinkedRelatedField(read_only=True, view_name='courseinfo-detail')

    class Meta:
        model = TeacherDetail
        # exclude = ('user', 'class_id')
        fields = '__all__'
        read_only_fields = ('id', 'user')


class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='localuser-detail',
                                               lookup_field='telephone')

    class Meta:
        model = SchoolDetail
        # exclude = ('user', 'class_id')
        fields = '__all__'
        read_only_fields = ('id', 'user')


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='localuser-detail',
                                               lookup_field='telephone')

    class Meta:
        model = OrganizationDetail
        # exclude = ('user', 'class_id')
        fields = '__all__'
        read_only_fields = ('id', 'user')


class ClassInfoSerializer(serializers.HyperlinkedModelSerializer):
    parent_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='parentdetail-detail')
    teacher_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='teacherdetail-detail')

    class Meta:
        model = ClassInformation
        # exclude = ('user', 'class_id')
        fields = ('id', 'provence', 'city', 'school', 'grade', 'classes', 'parent_in', 'teacher_in')
        read_only_fields = ('id', 'parent_in', 'teacher_in')
        extra_kwargs = {
           # 'url': {'lookup_field': 'user_id'},
        }


class CourseInfoSerializer(serializers.HyperlinkedModelSerializer):
    teacher_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='teacherdetail-detail')

    class Meta:
        model = CourseInformation
        # exclude = ('user', 'class_id')
        fields = ('id', 'course', 'intro', 'teacher_in')
        read_only_fields = ('id', 'course', 'intro', 'teacher_in')
        extra_kwargs = {
           # 'url': {'lookup_field': 'user_id'},
        }
