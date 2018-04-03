#coding=utf-8
'''
@author: zhangy
'''
from datetime import datetime

from utils import date


print date.today()
print date.tomorrow()
print datetime.now()
print date.get_old_date(date.today(), 7)
formatter = u"%Y-%m-%d %H:" + u"%s:00" %(datetime.now().minute / 10 * 10)
date_time = date.format_date(datetime.now(), formatter)
print date_time

