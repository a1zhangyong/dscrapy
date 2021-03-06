#coding=utf-8
'''

@author: zhangy
'''
class DescrapyConstant():
    DEFAULT_DSCRAPY_SERVER_PORT = 6800 
    DEFAULT_DSCRAPY_REDIS_IP = "127.0.0.1"
    DEFAULT_DSCRAPY_REDIS_PORT = 6379
    DEFAULT_DSCRAPY_REDIS_DB = 0
    DEFAULT_DSCRAPY_SETTINGS = "default"
    
    BASE_EGG_FILES_PATH = "egg_files_upload"
    LOG_FILE_PATH_DEBUG = "log/debug.log"
    
    TARGET_STATUS_DEPLOYED_NO = 0
    TARGET_STATUS_DEPLOYED_YES = 1
    
    TARGET_ONLINE_YES = 0
    TARGET_ONLINE_YES = 1
    
    TARGET_DELETED_NO = 0
    TARGET_DELETED_YES = 1
    
    QUEUE_DELETED_NO = 0
    QUEUE_DELETED_YES = 1
    QUEUE_TASKS_LIMIT = 5000000
    QUEUE_DATA_TYPE_LIST = 0
    QUEUE_DATA_TYPE_HASH = 1
    
    
    DEFAULT_NODE_USER = "huaw"
    DEFAULT_NODE_PASSWORD = "utn@360"
    WATCH_DISK_CMD = "df -hl"
    WATCH_MEMERY_CMD = "free -h"
    WATCH_CPU_CMD = "top -bi -n %d -d 0.02"
    COUNT_CPUS = "grep 'physical id' /proc/cpuinfo | sort -u| wc -l"
    
    DATE_TODAY = 1
    DATE_YESTERDAY = 2
    DATE_LAST_7_DAYS = 3
    DATE_LAST_30_DAYS = 4
    
    
    
    
    
    
    
    
    
    
    
    
    