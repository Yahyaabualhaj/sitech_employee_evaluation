# Generated by Django 3.2.3 on 2021-12-05 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation_processes', '0005_auto_20211205_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='evaluation_type',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='weight',
        ),
    ]