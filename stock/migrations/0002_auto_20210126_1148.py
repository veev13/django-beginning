# Generated by Django 3.1.5 on 2021-01-26 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='id',
        ),
        migrations.AlterField(
            model_name='stock',
            name='difference',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='stock',
            name='title',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stock',
            name='value',
            field=models.CharField(max_length=30),
        ),
    ]
