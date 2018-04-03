# -*- coding: utf-8 -*-
'''
Created on 2016-11-24

@author: Administrator
'''
from sqlalchemy import Column, String , Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JD(Base):
    __tablename__ = 'tb_jd_detail'

    id = Column(Integer, primary_key=True)
    shop_url = Column(String)
    detail_url = Column(String)
    province = Column(String)
    all_grades = Column(String)
    all_rate = Column(String)
    goods_grades = Column(String)
    goods_rate = Column(String)
    service_grades = Column(String)
    service_rate = Column(String)
    logistics_grades = Column(String)
    logistics_rate = Column(String)
    describ_grades = Column(String)
    describ_rate = Column(String)
    return_grades = Column(String)
    return_rate = Column(String)
    
    process_data = Column(String)
    process_data_average = Column(String)
    trade_data = Column(String)
    
    trade_data_average = Column(String)
    return_data = Column(String)
    return_data_average = Column(String)
    break_law_times = Column(String)
    
    is_success = Column(String)
    response_url = Column(String)
    create_time = Column(String)

