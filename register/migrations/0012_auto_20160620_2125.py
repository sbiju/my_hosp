# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-20 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0011_auto_20160614_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='patient',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='register.Patient'),
        ),
    ]