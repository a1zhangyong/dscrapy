#coding=utf-8
'''
@author: zhangy
'''
class JobException(Exception):
    def __init__(self,err='爬虫任务异常'):  
        Exception.__init__(self,err) 