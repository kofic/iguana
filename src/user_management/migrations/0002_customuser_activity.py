# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-01 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activity',
            field=models.TextField(default='{}'),
        ),
    ]