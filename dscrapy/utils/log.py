#coding=utf-8
'''
Created on 2014年2月11日

@author: ulindows
'''
import logging
from logging.handlers import RotatingFileHandler
import os
import traceback

from com.shop.utils import app


_LOGGER = None

def init(logname=None, autorun=False, level=logging.ERROR):
    '''
                初始化日志，autorun为False输出到console
    '''
    global _LOGGER

    if not logname:
        logname = 'log'

    #初始化log
    _LOGGER = logging.getLogger(logname)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    path = os.path.join(app.pwd(), logname)
    file_handle = RotatingFileHandler(path, maxBytes = 1024 * 1024)
    file_handle.setLevel(level)
    file_handle.setFormatter(fmt)
    _LOGGER.addHandler(file_handle)

    if not autorun:
        #界面显示
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter(fmt)
        _LOGGER.addHandler(console)

    _LOGGER.setLevel(level)

def debug(msg, *args, **kwargs):
    '''
    write debug log
    '''
    if _LOGGER:
        _LOGGER.debug(msg, *args, **kwargs)
    else:
        print(msg)
    

def info(msg, *args, **kwargs):
    '''
    write info log
    '''
    if _LOGGER:
        _LOGGER.info(msg, *args, **kwargs)
    else:
        print(msg)
        
def warning(msg, *args, **kwargs):
    '''
    write warning log
    '''
    if _LOGGER:
        _LOGGER.warning(msg, *args, **kwargs)
    else:
        print(msg)
        
def error(msg, *args, **kwargs):
    '''
    write error log and traceback
    '''
    if _LOGGER:
        _LOGGER.error(msg, *args, **kwargs)
        err = traceback.format_exc().strip()
        if err and err != 'None':
            _LOGGER.error(err)
    else:
        print(msg)

if __name__ == '__main__':
    init("test.log", False)
    info('info')
    error('这是一个测试')
