# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20151229_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_id',
            field=models.CharField(default='', max_length=10),
        ),
    ]