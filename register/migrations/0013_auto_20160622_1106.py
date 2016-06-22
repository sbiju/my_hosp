# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-22 05:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0012_auto_20160620_2125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-time_billed']},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='time_discharged',
            new_name='time_billed',
        ),
        migrations.AddField(
            model_name='patient',
            name='time_discharged',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
