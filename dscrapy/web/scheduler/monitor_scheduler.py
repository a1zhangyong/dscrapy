#coding=utf8
'''
@author: zhangy
'''

import redis
from utils.mysqldb import DBUtil



class MonitorScheduler():
    def __init__(self):
        self.db = DBUtil()
        self.db.init("192.168.108.123", "root", "root", "spider_redis", False)
        
    def count_queue(self):
        sql = "select spider_name, queue_name, queue_db from app_queue where deleted = 0 group by queue_name"
        queues = self.db.query(sql)
        for queue in queues:
            spider_name = queue[0]
            queue_name = queue[1]
            queue_db = queue[2]
            self.Redis = redis.StrictRedis(host="192.168.108.120", port=6379, db=queue_db)
            queue_count = self.Redis.llen(queue_name)
            insert_sql = "insert into app_monitor (spider_name, queue_name, tasks_count, create_time) values('%s', '%s', %d, CURRENT_TIMESTAMP())" %(spider_name, queue_name, queue_count)
            self.db.save_or_update(insert_sql)
            
    def start(self):
        self.count_queue()

#MonitorScheduler().start()            
            
            
            
            
            
            
            
            
            