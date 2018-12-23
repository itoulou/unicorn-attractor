# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-22 14:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('issue_tracker', '0019_auto_20181222_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 22, 14, 29, 10, 858286, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 12, 22, 14, 29, 10, 855805, tzinfo=utc), null=True),
        ),
    ]
