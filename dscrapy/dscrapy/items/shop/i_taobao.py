#coding=utf-8
'''
Created on 2016-11-24

@author: Administrator
'''
from scrapy import Item, Field

class TaoBaoItem(Item):
    shop_url = Field()
    detail_url = Field()
    goods_rate = Field()
    recent_month_total_rate = Field()
    recent_month_main_rate = Field()
    recent_month_not_main_rate = Field()
    recent_half_year_total_rate = Field()
    recent_half_year_main_rate = Field()
    recent_half_year_not_main_rate = Field()
    ago_half_year_total_rate = Field()
    ago_half_year_main_rate = Field()
    ago_half_year_not_main_rate = Field()
    cur_main_brand = Field()
    cur_main_brand_rate = Field()
    charge = Field()
    discrible_rate = Field()
    service_rate = Field()
    logistics_rate = Field()
    is_success = Field()
    response_url = Field()
    service_data_url = Field()
    create_time = Field()
    
    
    
