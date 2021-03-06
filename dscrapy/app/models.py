# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Targets(models.Model):
    target_name = models.CharField(max_length=100)
    project_name = models.CharField(max_length=200)
    host_ip = models.CharField(max_length=50)
    host_port = models.CharField(max_length=10)
    latest_version = models.CharField(max_length=200)
    status = models.IntegerField()
    is_online = models.IntegerField()
    deleted = models.IntegerField()
    create_time = models.DateTimeField()
    lastupdatetime = models.DateTimeField()
    
class Queue(models.Model):
    queue_name = models.CharField(max_length=200)
    spider_name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    queue_db = models.IntegerField()
    queue_ip = models.CharField(max_length=50)
    queue_port = models.CharField(max_length=10)
    total_submit = models.IntegerField()
    queue_describ = models.CharField(max_length=500)
    deleted = models.IntegerField()
    create_time = models.DateTimeField()

class Monitor(models.Model):
    spider_name = models.CharField(max_length=200)
    queue_name = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    tasks_count = models.IntegerField()
    create_time = models.DateTimeField()
    






