# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-24 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default=False, null=True),
        ),
    ]
