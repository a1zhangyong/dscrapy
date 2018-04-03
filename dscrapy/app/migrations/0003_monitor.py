# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170801_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spider_name', models.CharField(max_length=200)),
                ('queue_name', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('tasks_count', models.IntegerField()),
                ('create_time', models.DateTimeField()),
            ],
        ),
    ]
