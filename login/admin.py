"""
my custom user admin according to local user table
author:Neo
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.admin import GroupAdmin
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from login.models import LocalUser
from login.models import TeacherDetail
from login.models import ParentDetail
from login.models import SchoolDetail
from login.models import OrganizationDetail
from login.models import ClassInformation
from login.models import CourseInformation


# Register your models here.
class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = get_user_model()
        fields = ("telephone", "status")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    error_messages = {
        'username_unique': _("username already exist."),
        'email_unique': _("email already exist."),
    }

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def clean_username(self):
        # username could be unique if not none
        username = self.cleaned_data.get("username")
        if username and username != self.instance.username and \
                self.Meta.model.objects.all().filter(username=username):
            raise forms.ValidationError(
                self.error_messages['username_unique'],
                code='invalid',
            )
        return username

    def clean_email(self):
        # email could be unique if not none
        email = self.cleaned_data.get("email")
        if email and email != self.instance.email and self.Meta.model.objects.all().filter(email=email):
            raise forms.ValidationError(
                self.error_messages['email_unique'],
                code='invalid',
            )
        return email


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('telephone', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'email', 'social_id', 'status')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'status', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('telephone', 'username', 'email', 'social_id', 'status', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('telephone', 'username', 'email')
    ordering = ('telephone', 'username',)
    filter_horizontal = ('groups', 'user_permissions',)


# user_detail admin
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('user', 'real_name', 'nick_name', 'contact_phone', 'avatar'),
                           'class_id', 'intro', 'course')}),
        (_('status'), {'fields': ('is_online', 'is_identify', 'is_adviser')}),
    )
    readonly_fields = (
        'record_count', 'question_count', 'answer_count', 'forward_count',
        'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
        'msg_count', 'review_count', 'is_online'
    )
    list_display = ('user_id', 'real_name', 'nick_name', 'contact_phone', 'avatar',
                    'class_id', 'intro', 'course', 'is_adviser')
    list_filter = ['is_online', 'is_identify', 'is_adviser']
    search_fields = ('user', 'real_name', 'class_id')


# user_detail admin
class SchoolAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('user', 'school_name', 'contact_phone', 'avatar'),
                           'intro', 'courses')}),
        (_('status'), {'fields': ('is_online', 'is_identify', 'identity')}),
    )
    readonly_fields = (
        'record_count', 'question_count', 'answer_count', 'forward_count',
        'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
        'msg_count', 'review_count', 'is_online'
    )
    list_display = ('user_id', 'school_name', 'contact_phone', 'avatar',
                    'intro', 'courses', 'identity')
    list_filter = ['is_online', 'is_identify']
    search_fields = ('user', 'school_name', 'contact_phone')


# user_detail admin
class ParentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('user', 'real_name', 'nick_name', 'child_name', 'avatar'),
                           'class_id', 'intro')}),
        (_('status'), {'fields': ('is_online',)}),
    )
    readonly_fields = (
        'record_count', 'question_count', 'answer_count', 'forward_count',
        'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
        'msg_count', 'review_count', 'is_online'
    )
    list_display = ('user_id', 'real_name', 'nick_name', 'child_name', 'avatar',
                    'intro', 'class_id')
    list_filter = ['is_online']
    search_fields = ('user', 'real_name', 'child_name')


# user_detail admin
class OrganizationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (('user', 'real_name', 'contact_phone', 'avatar'), 'intro')}),
        (_('status'), {'fields': ('is_online', 'is_identify')}),
    )
    readonly_fields = (
        'record_count', 'question_count', 'answer_count', 'forward_count',
        'dig_count', 'bury_count', 'visit_count', 'follower_count', 'followee_count',
        'msg_count', 'review_count', 'is_online'
    )
    list_display = ('user_id', 'real_name', 'contact_phone', 'avatar',
                    'intro')
    list_filter = ['is_online', 'is_identify']
    search_fields = ('user', 'real_name', 'contact_phone')


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'provence', 'city', 'school', 'grade', 'classes')
    search_fields = ('classes',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'intro')
    search_fields = ('course',)


# admin.site.register(Group, GroupAdmin)
admin.site.register(LocalUser, MyUserAdmin)
admin.site.register(TeacherDetail, TeacherAdmin)
admin.site.register(SchoolDetail, SchoolAdmin)
admin.site.register(ParentDetail, ParentAdmin)
admin.site.register(OrganizationDetail, OrganizationAdmin)
admin.site.register(ClassInformation, ClassAdmin)
admin.site.register(CourseInformation, CourseAdmin)
