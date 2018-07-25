# coding:utf-8
"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModiftyView
from organization.views import OrgView
from django.views.static import serve
from mxonline.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url(r'^login/$', TemplateView.as_view(template_name='login.html'), name='login')
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active_user'),
    # url(r'^send_email/$', TemplateView.as_view(template_name='send_active_email.html'), name='send_active_email')
    # url(r'^send_email/$', SendEmailView.as_view(), name='send_active_email')
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModiftyView.as_view(), name='modify_pwd'),

    # 机构列表
    # url(r'^org_list/$', OrgView.as_view(), name='org_list'),
    url(r'^org/', include('organization.urls', namespace='org')),

    # 课程列表
    url(r'^courses/', include('courses.urls', namespace='courses')),

    # 机构组织列表图片
    url(r'^media/(?P<path>.*)/$', serve, {'document_root': MEDIA_ROOT}),
]
