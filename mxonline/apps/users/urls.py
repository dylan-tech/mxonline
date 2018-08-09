# coding:utf-8
__author__ = 'Dylan'

from django.conf.urls import url
from .views import UserInfoView, UpdateImageView, UpdatePWDView, SendEmailCodeView
from .views import UpdateEmailView, MyCoursesView
from .views import MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessageView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', UpdateImageView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UpdatePWDView.as_view(), name='update_pwd'),
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    url(r'^mycourses/$', MyCoursesView.as_view(), name='mycourses'),

    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),
]
