# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from app.models import Targets, Queue, Monitor
 
# Register your models here.
admin.site.register([Targets, Queue, Monitor])
