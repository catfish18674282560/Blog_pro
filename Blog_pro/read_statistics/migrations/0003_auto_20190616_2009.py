# Generated by Django 2.2 on 2019-06-16 12:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0002_auto_20190601_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdatenum',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 16)),
        ),
    ]