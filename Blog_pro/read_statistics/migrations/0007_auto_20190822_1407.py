# Generated by Django 2.2.3 on 2019-08-22 06:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0006_auto_20190730_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdatenum',
            name='date',
            field=models.DateField(default=datetime.date(2019, 8, 22)),
        ),
    ]