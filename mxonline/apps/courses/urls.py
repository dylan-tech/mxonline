# coding:utf-8
__author__ = 'Dylan'

from django.conf.urls import url
from .views import CoursesView

urlpatterns = [
    url(r'list/$', CoursesView.as_view(), name='courses_list')
]