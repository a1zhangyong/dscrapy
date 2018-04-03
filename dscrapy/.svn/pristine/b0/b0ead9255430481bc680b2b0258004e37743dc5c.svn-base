# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

# 初始化数据库连接:
#engine = create_engine('mysql+mysqldb://root:root123@115.159.149.177:3306/bjx?charset=utf8')
engine = create_engine('mysql+mysqldb://root:root@192.168.108.123:3306/spider_redis?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化redis数据库连接
Redis = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
Redis.client_setname('jd_detail')

