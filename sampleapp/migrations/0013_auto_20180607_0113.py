# Generated by Django 2.0.3 on 2018-06-06 19:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0012_auto_20180606_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 6, 7, 1, 13, 14, 320828)),
        ),
    ]