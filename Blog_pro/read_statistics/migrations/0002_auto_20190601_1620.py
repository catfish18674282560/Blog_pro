# Generated by Django 2.0.13 on 2019-06-01 08:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdatenum',
            name='date',
            field=models.DateField(default=datetime.date(2019, 6, 1)),
        ),
    ]
