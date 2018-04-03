#coding=utf-8
'''
Created on 2015-3-16

@author: xuji
'''

import datetime
import time
import re


FORMAT_DATE_NORMAL = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE_ONLY = "%Y-%m-%d"
FORMAT_DATE_UTC = "%Y-%m-%dT%H:%M:%SZ"

def parse_date(src_datestr, formatter):
    return datetime.datetime.strptime(src_datestr,formatter)

def format_date(src_date, formatter):
    return src_date.strftime(formatter)

def today():
    return datetime.date.today()

def get_old_date(srcdate,datediff):
    return srcdate - datetime.timedelta(days=datediff)

def get_future_date(srcdate,datediff):
    return srcdate + datetime.timedelta(days=datediff)

def yesterday():
    return get_old_date(datetime.date.today(),1)

def tomorrow():
    return get_future_date(datetime.date.today(),1)

def str2date(datestr):
    """
    convert datestr to datetime.date
    '2015-04-05' ==> 2015-04-05
    """
    date_array = datestr.split('-')
    return datetime.date(int(date_array[0]), int(date_array[1]), int(date_array[2]))

def date2str(src_date, formatter = FORMAT_DATE_ONLY):
    return format_date(src_date, formatter)

def datetime2str(src_datetime, formatter = FORMAT_DATE_NORMAL):
    return format_date(src_datetime, formatter)

def timestamp2str(src_timestamp, fromatter = FORMAT_DATE_NORMAL):
    return time.strftime(fromatter,time.localtime(src_timestamp))

def local2UTC(lt):
    '''local time to utc'''
    time_struct = time.mktime(lt.timetuple())
    utc = datetime.datetime.utcfromtimestamp(time_struct)
    return utc

def now_str():
    return datetime2str(datetime.datetime.now())

def now_utc_str():
    return datetime2str(local2UTC(datetime.datetime.now()), FORMAT_DATE_UTC)

def daysdiff(old_date, new_date): 
    if old_date == new_date :
        return 0
    return int(re.search('(-?\d+)\s+day',str(new_date-old_date)).group(1))

def get_now_time():
    return time.strftime(FORMAT_DATE_NORMAL,time.localtime(time.time()))

if __name__ == '__main__':
    print yesterday()
    print today()
    print tomorrow()
    print now_str()
    print now_utc_str()
    print daysdiff(str2date('2016-04-27'), str2date('1983-01-01'))
