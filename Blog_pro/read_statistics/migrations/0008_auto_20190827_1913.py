# Generated by Django 2.2.2 on 2019-08-27 11:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0007_auto_20190822_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdatenum',
            name='date',
            field=models.DateField(default=datetime.date(2019, 8, 27)),
        ),
    ]
