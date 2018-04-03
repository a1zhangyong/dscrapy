#coding=utf-8
'''
Created on 2016-4-29

@author: admin
'''

import sys
import threading
import time
from com.shop.utils import date
from functools import wraps
import functools
from com.shop.utils import log


class KThread(threading.Thread):

    """A subclass of threading.Thread, with a kill()

    method.

    

    Come from:

    Kill a thread in Python: 

    http://mail.python.org/pipermail/python-list/2004-May/260937.html

    """

    def __init__(self, *args, **kwargs):

        threading.Thread.__init__(self, *args, **kwargs)

        self.killed = False



    def start(self):

        """Start the thread."""

        self.__run_backup = self.run

        self.run = self.__run      # Force the Thread to install our trace.

        threading.Thread.start(self)



    def __run(self):

        """Hacked run function, which installs the

        trace."""

        sys.settrace(self.globaltrace)

        self.__run_backup()

        self.run = self.__run_backup



    def globaltrace(self, frame, why, arg):

        if why == 'call':

            return self.localtrace

        else:

            return None



    def localtrace(self, frame, why, arg):

        if self.killed:

            if why == 'line':

                raise SystemExit()

        return self.localtrace



    def kill(self):

        self.killed = True
        

class Timeout(Exception):

    """function run timeout"""


def timeout(seconds):

    """超时装饰器，指定超时时间

    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):

        """真正的装饰器"""

        

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):

            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        
        @wraps(func)
        def _func(*args, **kwargs):

            result = []

            new_kwargs = { # create new args for _new_func, because we want to get the func return val to result list

                'oldfunc': func,

                'result': result,

                'oldfunc_args': args,

                'oldfunc_kwargs': kwargs

            }
            

            thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)

            thd.start()

            thd.join(seconds)

            alive = thd.isAlive()

            thd.kill() # kill the child thread

            if alive:

                raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
            
            elif len(result) > 0 :
                
                return result[0]

        _func.__name__ = func.__name__

        _func.__doc__ = func.__doc__

        return _func

    return timeout_decorator

def timeit(func):
    """
                函数耗时
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        end_time = time.time()
        
        time_used = int(round((end_time-start_time)*1000))
        
        log.info(u"[%s] function %s used %d ms." % (date.now_str(),func.__name__,time_used))
        
        return result
        
    return wrapper

def memo(fn):
    """
                给函数调用做缓存
    """
    cache = {}
    miss = object()
 
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = cache.get(args, miss)
        if result is miss:
            result = fn(*args, **kwargs)
            cache[args] = result
        return result
 
    return wrapper

def logger(message):
    """
                输出日志
    """
    def log_decorator(func):
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log.info(message)
            return func(*args, **kwargs)
        return wrapper
    
    return log_decorator