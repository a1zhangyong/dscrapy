#coding=utf-8
'''
Created on 2014-2-2

@author: xuji
'''
import ConfigParser
from abc import abstractmethod, ABCMeta
import logging
import os
import sys
import traceback

import log
from util import pwd, singleton
import util


class Singleton(object):
    '''
    鍗曚緥妯″紡
    '''
    
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
    

class ConfigObj(object):
    '''
    Config鎶借薄瀵硅薄
    '''
    __metaclass__ = ABCMeta

    __DICT_LISTENER = {}
    
    def __init__(self):
        '''
        Constructor
        '''
        self.init()
        
    
    def init(self):
        cfgStore = self.get_configstore()
        cfgStore.get_fromstore(self)
            
    def set_field(self, field, value, ignore_null):
        
        if not hasattr(self, field):
            return False
        
        if not value:
            if not ignore_null:
                setattr(self, field, value)
                return True
        
        if isinstance(getattr(self, field), str):
            setattr(self, field, str(value))
        elif isinstance(getattr(self, field), bool):
            setattr(self, field, self.str2bool(value))
        elif isinstance(getattr(self, field), int):
            setattr(self, field, int(value))
        elif isinstance(getattr(self, field), float):
            setattr(self, field, float(value))
        else:
            return False
        
        return True
            
    def str2bool(self, value):
        
        if cmp('true', value.lower()) == 0:
            return True
        
        if cmp('on', value.lower()) == 0:
            return True
        
        if cmp('1', value.lower()) == 0:
            return True
        
        return False
    
        
    
    def add_listenler(self, listener):
        
        if listener is None:
            return
        
        listeners = ConfigObj.__DICT_LISTENER.get(self)
        if listeners is None:
            listeners = []
            listeners.append(listener)
            ConfigObj.__DICT_LISTENER[self] = listeners
        else:
            try:
                listeners.index(listener)
            except ValueError:
                listeners.append(listener)
    
    def remove_listener(self, listener):
        if listener is None:
            return
        
        listeners = ConfigObj.__DICT_LISTENER.get(self)
        if not (listeners is None):
            listeners.remove(listener)
            
    
    def rollback_listener(self):
        
        self.get_configstore().get_fromstore(self)
        
        listeners = ConfigObj.__DICT_LISTENER.get(self)
        if not (listeners is None):
            for listener in listeners:
                listener.rollback_change(self)
        
    def beforeUpdate(self):
        
        listeners = ConfigObj.__DICT_LISTENER.get(self)
        if not (listeners is None):
            for listener in listeners:
                try:
                    listener.on_change(self)
                except:
                    #涓嶆帴鏀舵柊鐨勫彉鏇达紝鍥炴粴宸茬粡onChange鐨刲istener
                    self.rollback_listener()
                    err = '鏇存柊閰嶇疆澶辫触,閰嶇疆鏁版嵁宸插洖婊氥�傚師鍥�:%s' % sys.exc_info()[1]
                    log.error(err)
                    raise Exception(err)
    
    def afterUpdate(self):
        
        listeners = ConfigObj.__DICT_LISTENER.get(self)
        if not (listeners is None):
            for listener in listeners:
                listener.commit_change(self)
    
    def save(self):
        try:
            self.verify_config()
        except:
            #楠岃瘉閰嶇疆澶辫触,鍏ㄩ儴鍥炴粴
            self.rollback_listener()
            err = '鏃犳晥鐨勯厤缃紝閰嶇疆鏁版嵁宸插洖婊氥�傚師鍥�:' % sys.exc_info()[1]
            log.error(err)
            raise Exception(err)
            
        #鏇存柊鍓嶈皟鐢ㄤ睛鍚��
        self.beforeUpdate()
        
        try:
            #淇濆瓨閰嶇疆鏂囦欢
            self.get_configstore().set_tostore(self)
        except:    
            #淇濆瓨閰嶇疆澶辫触锛屽叏閮ㄥ洖婊�
            self.rollback_listener()
            err = '淇濆瓨閰嶇疆澶辫触锛岄厤缃暟鎹凡鍥炴粴銆傚師鍥狅細%s' % sys.exc_info()[1]
            log.error(err)
            raise Exception(err)
            
        #鍥炶皟渚﹀惉鑰�
        self.afterUpdate()
        
    @abstractmethod
    def get_configstore(self):
        pass
    
    @abstractmethod
    def need_encrypt(self, name):
        return False
    
    @abstractmethod
    def verify_config(self):
        pass

class ConfigChangeListener(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_change(self, cfgObj):
        pass
    
    @abstractmethod
    def commit_change(self, cfgObj):
        pass
    
    @abstractmethod
    def rollback_change(self, cfgObj):
        pass
    
class ConfigStore(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    
    @abstractmethod
    def get_fromstore(self, cfgObj):
        pass
    
    @abstractmethod
    def set_tostore(self, cfgObj):
        pass
    
    
class IniFileConfigStore(ConfigStore):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self, path):
        '''
        Constructor
        '''
        super(IniFileConfigStore, self).__init__()
        self.path = path
  
    
    def get_fromstore(self, cfgObj):
        
        if cfgObj is None:
            return
        
        try:
            cfgName = self.get_cfgname(cfgObj)
            
            cfg = ConfigParser.SafeConfigParser()
            cfg.read(self.path)
            
            '''
            # ConfigParser璇诲彇opt鏃朵細鍏ㄩ儴灏忓啓澶勭悊锛屼細瀵艰嚧鏃犳硶鍖归厤ConfigObj鐨勬垚鍛樺彉閲�
            if cfg.has_section(cfgName):
                options = cfg.options(cfgName)
                for opt in options:
                    value = cfg.get(cfgName, opt)
                    if cfgObj.need_encrypt(opt):
                        value = self.decrypt(value)
                    cfgObj.set_field(opt, value, True)
            '''
            if cfg.has_section(cfgName):
                for k in cfgObj.__dict__:
                    if isinstance(getattr(cfgObj, k), str) \
                        or isinstance(getattr(cfgObj, k), bool) \
                        or isinstance(getattr(cfgObj, k), int) \
                        or isinstance(getattr(cfgObj, k), float):
                        
                        if cfg.has_option(cfgName, k):
                            value = cfg.get(cfgName, k)
                            if cfgObj.need_encrypt(k):
                                value = self.decrypt(value)
                            cfgObj.set_field(k, value, True)
            #}}
        except:
            log.error('浠庨厤缃枃浠跺垵濮嬪寲鏁版嵁澶辫触,鍘熷洜:%s' % str(sys.exc_info()[1]))
    
    
    def set_tostore(self, cfgObj):
        
        if None == cfgObj:
            return False
        
        try:
            cfgName = self.get_cfgname(cfgObj)
            
            cfg = ConfigParser.SafeConfigParser()
            cfg.read(self.path)
            
            if not cfg.has_section(cfgName):
                cfg.add_section(cfgName)
                
            for k in cfgObj.__dict__:
                if isinstance(getattr(cfgObj, k), str) \
                    or isinstance(getattr(cfgObj, k), bool) \
                    or isinstance(getattr(cfgObj, k), int) \
                    or isinstance(getattr(cfgObj, k), float):
                    
                    value = str(getattr(cfgObj, k))
                    if cfgObj.need_encrypt(k):
                        value = self.encrypt(value)
                    cfg.set(cfgName, k, value)

            with open(self.path, 'w+') as f:            
                cfg.write(f)
        except:
            err = str(sys.exc_info()[1])
            log.error('鍚戦厤缃枃浠跺啓鍏ユ暟鎹け璐�,鍘熷洜:%s' % err)
            raise Exception(err)
            

    
    def get_cfgname(self, cfgObj):
        return cfgObj.__class__.__name__
    
    @abstractmethod
    def encrypt(self, value):
        pass
    
    @abstractmethod
    def decrypt(self, value):
        pass
    
    
class DefaultConfigStore(IniFileConfigStore):
    '''
    classdocs
    '''
    def __init__(self, path):
        '''
        Constructor
        '''
        super(DefaultConfigStore, self).__init__(path)
        
    def encrypt(self, value):
        return value
    
    def decrypt(self, value):
        return value


def get_configstore():
    return DefaultConfigStore(os.path.join(pwd(), 'config.ini'))

    
@singleton
class LogCfg(ConfigObj):
    '''
    classdocs
    '''
            
    def __init__(self):
        '''
        Constructor
        '''
        self.logName   = 'info.log'
        self.logLevel  = 'INFO'
        self.autoRun   = False
        
        self.init()
        
    def get_configstore(self):
        return get_configstore()
    
    def need_encrypt(self, name):
        return False
    
    def verify_config(self):
        pass

    def getLogLevel(self):
        
        level = logging._levelNames.get(self.logLevel)
        
        if level is None:
            level = logging.ERROR
            
        return level



