"""bijian_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from login.routers import RegiserRouter, ReadOnlyRouter
from login import views
from django.contrib import admin

regrouter = RegiserRouter(trailing_slash=False)
regrouter.register(r'parents', views.ParentViewSet, )
regrouter.register(r'teachers', views.TeacherViewSet, )
regrouter.register(r'schools', views.SchoolViewSet, )
regrouter.register(r'organizations', views.OrganiztionViewSet, )

read_only = ReadOnlyRouter(trailing_slash=False)
read_only.register(r'classes', views.ClassInfoViewSet, base_name='classinfo')
read_only.register(r'courses', views.CourseInfoViewSet, base_name='courseinfo')

urlpatterns = [
    url(r'^api/$', views.api_root),
    url(r'^api/', include(regrouter.urls)),
    url(r'^api/', include(read_only.urls)),
    url(r'^api/users/$', views.UserInfoView.as_view(), name='localuser-list'),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += [
   url(r'^admin/', include(admin.site.urls)),
]
