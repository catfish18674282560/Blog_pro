# Generated by Django 2.2 on 2019-06-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='nickName',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='昵称'),
        ),
    ]
