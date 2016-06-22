# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-14 00:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_auto_20160613_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='auth_discharge',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True),
        ),
    ]