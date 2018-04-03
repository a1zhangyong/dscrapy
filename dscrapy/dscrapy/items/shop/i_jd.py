#coding=utf-8
'''
Created on 2016-11-24

@author: Administrator
'''
from scrapy import Item, Field

class JDItem(Item):
    shop_url = Field()
    detail_url = Field()
    province = Field()
    
    all_grades = Field()
    all_rate = Field()
    goods_grades = Field()
    goods_rate = Field()
    service_grades = Field()
    service_rate = Field()
    logistics_grades = Field()
    logistics_rate = Field()
    describ_grades = Field()
    describ_rate = Field()
    return_grades = Field()
    return_rate = Field()
    
    process_data = Field()
    process_data_average = Field()
    trade_data = Field()
    trade_data_average = Field()
    
    return_data = Field()
    return_data_average = Field()
    break_law_times = Field()
   
    is_success = Field()
    response_url = Field()
    create_time = Field()
    
    
    
