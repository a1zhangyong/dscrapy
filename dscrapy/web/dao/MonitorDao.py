#coding=utf8
'''
@author: zhangy
'''

from app.models import Monitor
import datetime
from utils import date
 
 
def addMonitor(monitor):
    monitor.save()
     
def findByQueueNameAndDate(queue_name, date_from, date_to):
    kwargs = {'queue_name':queue_name, 'create_time__range':(date_from, date_to)}
    return Monitor.objects.filter(**kwargs)
 
def findRecentlyQueuesCount():
    formatter = u"%Y-%m-%d %H:" + u"%s:00" %(datetime.datetime.now().minute / 10 * 10)
    date_time = date.format_date(datetime.datetime.now(), formatter)
    kwargs = {'create_time__gte':date_time}
    return Monitor.objects.filter(**kwargs).order_by("-tasks_count")


#查看倒数第二次记录的所有的队列信息
def findLastTwoQueuesCount():
    formatter = u"%Y-%m-%d %H:" + u"%s:00" %((datetime.datetime.now().minute / 10) * 10)
    date_time = date.format_date(datetime.datetime.now(), formatter)
    start_date = datetime.datetime.strptime(date_time, date.FORMAT_DATE_NORMAL) 
    old_date = date.format_date(start_date - datetime.timedelta(seconds=600))   #十分钟之前
    kwargs = {'create_time__gte':old_date}
    return Monitor.objects.filter(**kwargs).order_by("-tasks_count")

