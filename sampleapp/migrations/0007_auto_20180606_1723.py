# Generated by Django 2.0.3 on 2018-06-06 11:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleapp', '0006_auto_20180606_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2018, 6, 6, 17, 23, 15, 389138)),
        ),
    ]
