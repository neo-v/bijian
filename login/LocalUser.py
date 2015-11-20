"""
user table for bijian app

with fields:
django user fields + telephone

telephone is the USERNAME_FIELD

__author__ = 'Neo'

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
    """
    telephone = models.CharField(
        _('telephone'), max_length=30, unique=True,
        help_text=_('Required numbers only.'),
        error_messages={
            'unique': _("A user with that telephone already exists."),
        })

    username = models.CharField(
        _('username'), max_length=30, unique=True, blank=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    email = models.EmailField(
        _('email address'), blank=True, unique=True,
        error_messages={
            'unique': _("A user with that username already exists."),
        })

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
