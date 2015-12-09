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
from login.exceptions import KeyFoundError
import logging
# from rest_framework.validators import UniqueValidator

logger = logging.getLogger(__name__)


class CreateUserSerializer(serializers.ModelSerializer):
    """
    create user serializer input data
    include telephone password
    """
    class Meta:
        model = LocalUser
        fields = ('telephone', 'password', 'status')

    # def create(self, validated_data):
    #     """
    #     create user use serializer
    #     :param validated_data:
    #     :return:user instance
    #     """
    #     try:
    #         logger.debug('create user serializer :pick data')
    #         tel = validated_data['telephone']
    #         password = validated_data['password']
    #     except KeyError, e:
    #         logger.debug('create user serializer :keyError')
    #         raise KeyFoundError(e.__str__())
    #
    #     user = LocalUser(telephone=tel)
    #     user.set_password(password)
    #     user.save()
    #     return user


class FullParentSerializer(serializers.ModelSerializer):
    """
    full profile of parent detail for owner
    """
    user = serializers.StringRelatedField(read_only=True)
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail')

    class Meta:
        model = ParentDetail
        exclude = ('id', )
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online')


class BasicParentSerializer(serializers.ModelSerializer):
    """
    basic profile of parent detail for others
    """
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail',)

    class Meta:
        model = ParentDetail
        exclude = ('id', 'user')
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online')


class FullTeacherSerializer(serializers.ModelSerializer):

    # user = serializers.HyperlinkedRelatedField(read_only=True, view_name='localuser-detail',
    #                                            lookup_field='telephone')
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail')
    course = serializers.HyperlinkedRelatedField(read_only=True, view_name='courseinfo-detail')
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = TeacherDetail
        exclude = ('id', )
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify')


class BasicTeacherSerializer(serializers.ModelSerializer):

    # user = serializers.HyperlinkedRelatedField(read_only=True, view_name='localuser-detail',
    #                                            lookup_field='telephone')
    class_id = serializers.HyperlinkedRelatedField(queryset=ClassInformation.objects.all(),
                                                   view_name='classinfo-detail')
    course = serializers.HyperlinkedRelatedField(read_only=True, view_name='courseinfo-detail')

    class Meta:
        model = TeacherDetail
        exclude = ('id', 'user')
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify')


class FullSchoolSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SchoolDetail
        exclude = ('id', )
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify', 'identity')


class BasicSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolDetail
        exclude = ('id', 'user')
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify', 'identity')


class FullOrganizationSerializer(serializers.ModelSerializer):
    user = serializers.ModelSerializer(read_only=True)

    class Meta:
        model = OrganizationDetail
        exclude = ('id', )
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify', 'identity')


class BasicOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationDetail
        exclude = ('id', 'user')
        # fields = '__all__'
        read_only_fields = ('record_count', 'question_count', 'answer_count', 'forward_count',
                            'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
                            'msg_count', 'review_count', 'is_online', 'is_identify', 'identity')


class ClassInfoSerializer(serializers.HyperlinkedModelSerializer):
    parent_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='parentdetail-detail',
                                                    lookup_field='user_id')
    teacher_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='teacherdetail-detail',
                                                     lookup_field='user_id')

    class Meta:
        model = ClassInformation
        # exclude = ('user', 'class_id')
        fields = ('id', 'provence', 'city', 'school', 'grade', 'classes', 'parent_in', 'teacher_in')
        read_only_fields = ('id', 'parent_in', 'teacher_in')


class CourseInfoSerializer(serializers.HyperlinkedModelSerializer):
    teacher_in = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='teacherdetail-detail',
                                                     lookup_field='user_id')

    class Meta:
        model = CourseInformation
        # exclude = ('user', 'class_id')
        fields = ('id', 'course', 'intro', 'teacher_in')
        read_only_fields = ('id', 'course', 'intro', 'teacher_in')
        extra_kwargs = {
           # 'url': {'lookup_field': 'user_id'},
        }
