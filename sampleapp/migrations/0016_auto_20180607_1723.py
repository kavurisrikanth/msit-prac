# Generated by Django 2.0.3 on 2018-06-07 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0015_auto_20180607_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 6, 7, 17, 23, 13, 245859)),
        ),
    ]
