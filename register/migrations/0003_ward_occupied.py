# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-12 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20160611_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='ward',
            name='occupied',
            field=models.BooleanField(default=False),
        ),
    ]
