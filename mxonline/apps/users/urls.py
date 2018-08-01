# coding:utf-8
__author__ = 'Dylan'

from django.conf.urls import url
from .views import UserInfoView, UpdateImageView, UpdatePWDView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UpdateImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UpdatePWDView.as_view(), name='update_pwd')
]
