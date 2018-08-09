# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'机构名', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField(max_length=10, choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')),
                              verbose_name=u'课程难度')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u'课程类别')
    tags = models.CharField(max_length=20, verbose_name=u'课程标签', null=True, blank=True)
    need_know = models.CharField(max_length=100, verbose_name=u'课程需知', default='')
    to_learn = models.CharField(max_length=100, verbose_name=u'讲师提示', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()


class IsBannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    video = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(default='', max_length=50, verbose_name=u'视频链接')
    study_time = models.IntegerField(default=0, verbose_name=u'学习时长（分钟）')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'资源')
    download = models.FileField(upload_to='courses/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


