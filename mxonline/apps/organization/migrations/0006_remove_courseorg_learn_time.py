# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-20 10:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_courseorg_learn_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='learn_time',
        ),
    ]
