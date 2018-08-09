# coding:utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# from django.utils import timezone


class UserProfile(AbstractUser):
    name = models.CharField(max_length=50, default='', verbose_name=u'别名')
    birthday = models.DateField(verbose_name=u'出生日期', null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')), default=u'female')
    address = models.CharField(max_length=100, default='')
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username

    def get_unread_nums(self):
        from operation.models import UserMessage
        unread_nums = UserMessage.objects.filter(user=self.id, has_read=False)
        return unread_nums.count()


class EmailVerityCode(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'用户邮箱')
    send_type = models.CharField(choices=(('register', u'注册'), ('forget', u'找回密码'), ('update_email', u'更新邮箱')),
                                 max_length=20, verbose_name=u'类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')
    # send_date = models.DateField(default=timezone.now, verbose_name=u'发送月份', null=True)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}.{1}'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    url = models.URLField(max_length=100, verbose_name=u'访问地址')
    image = models.ImageField(max_length=100, upload_to='banner/%Y/%m', verbose_name=u'轮播图')
    index = models.IntegerField(default=100, verbose_name=u'轮播顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __unicode(self):
        return self.title


