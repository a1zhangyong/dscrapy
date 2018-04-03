# -*- coding: utf-8 -*-

from dscrapy.common.cfg.db_cfg import DBSession, Redis
from dscrapy.model.shop.m_jd import JD
from scrapy.exceptions import DropItem
import codecs
import json

# 去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('jd:%s' % item['detail_url']):
            raise DropItem("Duplicate jd found: %s" % item)
        else:
            Redis.set('jd:%s' % item['detail_url'],1)
            return item

# 存储到数据库
class DataBasePipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        jd = JD(
                    detail_url = item["detail_url"],
                    province = item["province"],
                    all_grades = item["all_grades"],
                    all_rate = item["all_rate"],
                    goods_grades = item["goods_grades"],
                    goods_rate = item["goods_rate"],
                    service_grades = item["service_grades"],
                    service_rate = item["service_rate"],
                    logistics_grades = item["logistics_grades"],
                    logistics_rate = item["logistics_rate"],
                    describ_grades = item["describ_grades"],
                    describ_rate = item["describ_rate"],
                    return_grades = item["return_grades"],
                    return_rate = item["return_rate"],
                    process_data = item["process_data"],
                    process_data_average = item["process_data_average"],
                    trade_data = item["trade_data"],
                    trade_data_average = item["trade_data_average"],
                    return_data = item["return_data"],
                    return_data_average = item["return_data_average"],
                    break_law_times = item["break_law_times"],
                    is_success=item["is_success"],
                    response_url=item["response_url"],
                    create_time=item["create_time"])
        self.session.add(jd)
        self.session.commit()

    def close_spider(self,spider):
        print "spider closed!................"
        self.session.close()

# 存储到文件
class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('/shop-spider/com/shop/files/jds.json', 'w+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode('unicode_escape'))
        return item
    
    
    
