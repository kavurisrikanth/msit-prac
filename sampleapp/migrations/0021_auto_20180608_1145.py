# Generated by Django 2.0.3 on 2018-06-08 06:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0020_auto_20180608_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 6, 8, 11, 45, 15, 9597)),
        ),
        migrations.AlterField(
            model_name='musicpiece',
            name='created',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 6, 8, 11, 45, 15, 9597)),
        ),
    ]
