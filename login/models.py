"""
models for bijian
author:Neo
"""

from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.conf import settings

# Create your models here.
# user table for bijian app
#
# with fields:
# django user fields + telephone
#
# telephone is the USERNAME_FIELD
#
# __author__ = 'Neo'


class LocalUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telephone, password, email,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not telephone:
            raise ValueError('The given telephone must be set')
        email = self.normalize_email(email)
        user = self.model(telephone=telephone, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, telephone, password=None, email=None, **extra_fields):
        return self._create_user(telephone, password, email, False, False,
                                 **extra_fields)

    def create_superuser(self, telephone, password, email, **extra_fields):
        return self._create_user(telephone, password, email, True, True,
                                 **extra_fields)


class LocalUser(AbstractBaseUser, PermissionsMixin):
    """
    extend telephone field to django User model
    support for open social platfrom to access
    """
    TEACHER = 'TC'
    SCHOOL = 'SC'
    ORGANIZATION = 'OG'
    PARENT = 'PR'
    VISITOR = 'VS'
    TYPE_CHOICES = (
        (TEACHER, 'teacher'),
        (SCHOOL, 'school'),
        (ORGANIZATION, 'organization'),
        (PARENT, 'parent'),
        (VISITOR, 'visitor'),
    )

    telephone = models.CharField(
        _('telephone'), max_length=30, unique=True,
        help_text=_('Required numbers only.'),
        error_messages={
            'unique': _("A user with that telephone already exists."),
        })
    # unique=True //control by logic code
    username = models.CharField(
        _('username'), max_length=30,  blank=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A username with that username already exists."),
        })

    email = models.EmailField(
        _('email address'), blank=True,
        error_messages={
            'unique': _("A email with that email already exists."),
        })
    # store as platform_openid
    social_id = models.CharField(_('social_id'), max_length=30, blank=True)
    type = models.CharField(_('type'), max_length=30, blank=True, choices=TYPE_CHOICES, default=PARENT)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = LocalUserManager()

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        :type kwargs: object
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_platform(self):
        """
        get user social platform
        :return: string platfrom
        """
        return self.social_id.split('_')[0]


# parent detail table
class ParentDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='parent_of')
    avatar = models.CharField(_('avatar'), max_length=256,  blank=True)
    intro = models.CharField(_('introduce'), max_length=256,  blank=True)

    child_name = models.CharField(_('child_name'), max_length=30,  blank=True)
    real_name = models.CharField(_('real_name'), max_length=30,  blank=True)
    nick_name = models.CharField(_('nick_name'), max_length=30,  blank=True)

    # personal data count
    record_count = models.PositiveIntegerField(_('record'), default=0)
    question_count = models.PositiveIntegerField(_('question'), default=0)
    answer_count = models.PositiveIntegerField(_('answer'), default=0)
    forward_count = models.PositiveIntegerField(_('forward'), default=0)
    dig_count = models.PositiveIntegerField(_('dig'), default=0)
    bury_count = models.PositiveIntegerField(_('bury'), default=0)
    visit_count = models.PositiveIntegerField(_('visited'), default=0)

    follower_count = models.PositiveIntegerField(_('follower'), default=0)
    followee_count = models.PositiveIntegerField(_('followee'), default=0)

    msg_count = models.PositiveIntegerField(_('message'), default=0)
    review_count = models.PositiveIntegerField(_('review'), default=0)

    # personal class info
    class_id = models.ForeignKey('ClassInformation', related_name='parent_in')

    is_online = models.BooleanField(_('online'), default=False)

    def __str__(self):
        return self.child_name


# teacher detail table
class TeacherDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='teacher_of')
    avatar = models.CharField(_('avatar'), max_length=256,  blank=True)
    intro = models.CharField(_('introduce'), max_length=256,  blank=True)
    course = models.ForeignKey('CourseInformation', related_name='teacher_in')

    real_name = models.CharField(_('real_name'), max_length=30,  blank=True)
    nick_name = models.CharField(_('nick_name'), max_length=30,  blank=True)
    contact_phone = models.CharField(_('contact_phone'), max_length=30,  blank=True,
                                     help_text=_('Required numbers only.'))

    record_count = models.PositiveIntegerField(_('record'), default=0)
    question_count = models.PositiveIntegerField(_('question'), default=0)
    answer_count = models.PositiveIntegerField(_('answer'), default=0)
    forward_count = models.PositiveIntegerField(_('forward'), default=0)
    dig_count = models.PositiveIntegerField(_('dig'), default=0)
    bury_count = models.PositiveIntegerField(_('bury'), default=0)
    visit_count = models.PositiveIntegerField(_('visited'), default=0)

    follower_count = models.PositiveIntegerField(_('follower'), default=0)
    followee_count = models.PositiveIntegerField(_('followee'), default=0)

    msg_count = models.PositiveIntegerField(_('message'), default=0)
    review_count = models.PositiveIntegerField(_('review'), default=0)

    class_id = models.ForeignKey('ClassInformation', related_name='teacher_in')
    is_online = models.BooleanField(_('online'), default=False)

    is_identify = models.BooleanField(_('identify'), default=False)
    is_adviser = models.BooleanField(_('class adviser'), default=False)

    def __str__(self):
        return self.real_name


# org detail table
class OrganizationDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='organization_of')
    avatar = models.CharField(_('avatar'), max_length=256,  blank=True)
    intro = models.CharField(_('introduce'), max_length=256,  blank=True)

    real_name = models.CharField(_('real_name'), max_length=30,  blank=True)
    contact_phone = models.CharField(_('contact_phone'), max_length=30,  blank=True,
                                     help_text=_('Required numbers only.'))

    record_count = models.PositiveIntegerField(_('record'), default=0)
    question_count = models.PositiveIntegerField(_('question'), default=0)
    answer_count = models.PositiveIntegerField(_('answer'), default=0)
    forward_count = models.PositiveIntegerField(_('forward'), default=0)
    dig_count = models.PositiveIntegerField(_('dig'), default=0)
    bury_count = models.PositiveIntegerField(_('bury'), default=0)
    visit_count = models.PositiveIntegerField(_('visited'), default=0)

    follower_count = models.PositiveIntegerField(_('follower'), default=0)
    followee_count = models.PositiveIntegerField(_('followee'), default=0)

    msg_count = models.PositiveIntegerField(_('message'), default=0)
    review_count = models.PositiveIntegerField(_('review'), default=0)

    is_identify = models.BooleanField(_('identify'), default=False)
    identity = models.CharField(_('identity'), max_length=256,  blank=True)

    is_online = models.BooleanField(_('online'), default=False)

    def __str__(self):
        return self.real_name


# school detail table
class SchoolDetail(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='school_of')
    avatar = models.CharField(_('avatar'), max_length=256,  blank=True)
    intro = models.CharField(_('introduce'), max_length=256,  blank=True)
    courses = models.CharField(_('courses'), max_length=256,  blank=True)

    school_name = models.CharField(_('real_name'), max_length=30,  blank=True)
    contact_phone = models.CharField(_('contact_phone'), max_length=30,  blank=True,
                                     help_text=_('Required numbers only.'))

    record_count = models.PositiveIntegerField(_('record'), default=0)
    question_count = models.PositiveIntegerField(_('question'), default=0)
    answer_count = models.PositiveIntegerField(_('answer'), default=0)
    forward_count = models.PositiveIntegerField(_('forward'), default=0)
    dig_count = models.PositiveIntegerField(_('dig'), default=0)
    bury_count = models.PositiveIntegerField(_('bury'), default=0)
    visit_count = models.PositiveIntegerField(_('visited'), default=0)

    follower_count = models.PositiveIntegerField(_('follower'), default=0)
    followee_count = models.PositiveIntegerField(_('followee'), default=0)

    msg_count = models.PositiveIntegerField(_('message'), default=0)
    review_count = models.PositiveIntegerField(_('review'), default=0)

    is_identify = models.BooleanField(_('identify'), default=False)
    identity = models.CharField(_('identity'), max_length=256,  blank=True)

    is_online = models.BooleanField(_('online'), default=False)

    def __str__(self):
        return self.school_name


# class information table
class ClassInformation(models.Model):
    provence = models.CharField(_('provence'), max_length=50,  blank=True,
                                help_text=_('provence information about your child class'))
    city = models.CharField(_('city'), max_length=50,  blank=True,
                            help_text=_('city information about your child class'))
    school = models.CharField(_('school'), max_length=50,  blank=True,
                              help_text=_('school information about your child class'))
    grade = models.CharField(_('grade'), max_length=50,  blank=True,
                             help_text=_('grade information about your child class'))
    classes = models.CharField(_('class'), max_length=50,  blank=True,
                               help_text=_('class information'))

    def __str__(self):
        return str(self.id)


# course information table
class CourseInformation(models.Model):
    course = models.CharField(_('course'), max_length=50,
                              help_text=_('school courses'))
    intro = models.CharField(_('introduction'), max_length=256, blank=True)

    def __str__(self):
        return str(self.id)
