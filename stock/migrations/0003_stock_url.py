# Generated by Django 3.1.5 on 2021-01-26 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_auto_20210126_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='url',
            field=models.URLField(default='https://naver.com'),
            preserve_default=False,
        ),
    ]
