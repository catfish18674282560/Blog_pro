# Generated by Django 2.2.3 on 2019-08-28 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app1', '0004_auto_20190827_1923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-creation_time'], 'verbose_name': '博客', 'verbose_name_plural': '博客'},
        ),
        migrations.AlterModelOptions(
            name='blog_type',
            options={'verbose_name': '博客类型', 'verbose_name_plural': '博客类型'},
        ),
    ]