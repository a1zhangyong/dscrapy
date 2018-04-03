# -*- coding: utf-8 -*-
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess
from spiders.jd_spider import JDSpider

my_settings = Settings()

# crawl my_settings
#这里ITEM_PIPELINES是一个Python字典，其中key保存的pipline类在项目中的位置，value为整型值，确定了他们运行的顺序，item按数字从低到高的顺序，通过pipeline，通常将这些数字定义在0-1000范围内。
my_settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
my_settings.set("ITEM_PIPELINES" , {
    'dscrapy.pipelines.shop.jd_pipelines.DataBasePipeline': 600,
    #'com.shop.pipelines.shop.jd_pipelines.DuplicatesPipeline': 400
})
#设置下载图片目录
#my_settings.set("IMAGES_STORE", "F:\school_imgs")
#设置refer
my_settings.set("DEFAULT_REQUEST_HEADERS",{
    'Referer':'http://mall.jd.com/'                                        
})

#失败重试
#my_settings.set("RETRY_HTTP_CODES", [500, 503, 504, 400, 403, 404, 408, 301, 302])
#my_settings.set("RETRY_TIMES ", 3)

#放ban措施
#1.动态user-agent
my_settings.set("DOWNLOADER_MIDDLEWARES", {
    #'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 80,        #失败重试                                    
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
    #'com.shop.protect.middlewares.RotateUserAgentMiddleware' :200,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #'com.shop.protect.middlewares.ProxyMiddleware': 100,
})
#2.禁用cookies
#my_settings.set("COOKIES_ENABLES", False)

#3.1 动态ip[crawlera]
#my_settings.set("DOWNLOADER_MIDDLEWARES", {
#    'scrapy_crawlera.CrawleraMiddleware': 100
#})
#my_settings.set("CRAWLERA_ENABLED", True)
#my_settings.set("CRAWLERA_APIKEY", "7fd0ff8cd3874db5b15565265d3a327f")
#my_settings.set("CONCURRENT_REQUESTS", 32)
#my_settings.set("CONCURRENT_REQUESTS_PER_DOMAIN", 32)
#my_settings.set("AUTOTHROTTLE_ENABLED", False)
#my_settings.set("DOWNLOAD_TIMEOUT", 600)
#3.2 动态ip
#my_settings.set("DOWNLOADER_MIDDLEWARES", {
#    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
#    'com.shop.protect.middlewares.ProxyMiddleware': 100,
#})

#redis config 
#启用Redis调度存储请求队列
#my_settings.set("scrapy_redis.scheduler.Scheduler", True) 
#不清除Redis队列、这样可以暂停/恢复 爬取
my_settings.set("SCHEDULER_PERSIST", True)
my_settings.set("REDIS_URL", 'redis://192.168.108.120:6379')

my_settings.set("ROBOTSTXT_OBEY", False)
my_settings.set("DOWNLOAD_DELAY", 1)

#启动爬虫,调试用
process = CrawlerProcess(my_settings)
process.crawl(JDSpider)
process.start()

