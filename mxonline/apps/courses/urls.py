# coding:utf-8
__author__ = 'Dylan'

from django.conf.urls import url
from .views import CoursesView, CourseDetailView, CourseInfoView, CommentsView, AddCommentView, VideoPlayView

urlpatterns = [
    url(r'^list/$', CoursesView.as_view(), name='courses_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='courses_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='courses_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='courses_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^video/$', VideoPlayView.as_view(), name='video_play'),

]