# -*- coding: utf-8 -*-
from sqlalchemy import Column, String , Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class Proxy(Base):
    __tablename__ = 'tb_data_proxy'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    port = Column(Integer)
    type = Column(String)
    is_school_valid = Column(Integer)
    is_taobao_valid = Column(Integer)
    check_result = Column(String)

