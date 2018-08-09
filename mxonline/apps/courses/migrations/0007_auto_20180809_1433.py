# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-08-09 14:33
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_is_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsBannerCourse',
            fields=[
            ],
            options={
                'verbose_name': '\u8f6e\u64ad\u8bfe\u7a0b',
                'proxy': True,
                'verbose_name_plural': '\u8f6e\u64ad\u8bfe\u7a0b',
            },
            bases=('courses.course',),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='\u8bfe\u7a0b\u8be6\u60c5'),
        ),
    ]