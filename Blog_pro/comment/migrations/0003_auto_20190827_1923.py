# Generated by Django 2.2.2 on 2019-08-27 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20190525_2211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time'], 'verbose_name': '评论', 'verbose_name_plural': ''},
        ),
    ]
