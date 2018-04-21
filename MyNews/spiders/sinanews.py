# -*- coding: utf-8 -*-
import json
import time
from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
from ..headers import qqheaders

class SinaNewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (sinanews:start_urls)."""

    '''
    start_url = "http://feed.mix.sina.com.cn/api/roll/get?pageid=153"
    '''
    name = 'sinanews'
    redis_key = 'sinanews:start_urls'
    tags_list = ['ent','sports','finance','tech']
    tagnum_list = [2513,2512,2516,2515]

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('sina.com.cn', 'news.sina.com.cn')
        self.allowed_domains = filter(None, domain.split(','))
        super(SinaNewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        for j in range(10):
            for i in self.tagnum_list:
                if i == 2513:
                    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid='+str(i)+'&k=&num=50&page='+str(j)
                    yield Request(url, callback=self.parsepage, meta={'tag':'ent'}, dont_filter=True)
                if i == 2512:
                    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=' + str(i) + '&k=&num=50&page=' + str(j)
                    yield Request(url, callback=self.parsepage, meta={'tag': 'sports'}, dont_filter=True)
                if i == 2516:
                    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=' + str(
                        i) + '&k=&num=50&page=' + str(j)
                    yield Request(url, callback=self.parsepage, meta={'tag': 'finance'}, dont_filter=True)
                if i == 2515:
                    url = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=' + str(
                        i) + '&k=&num=50&page=' + str(j)
                    yield Request(url, callback=self.parsepage, meta={'tag': 'tech'}, dont_filter=True)

    def parsepage(self,response):
        tag = response.meta['tag']
        newsjson = json.loads(response.text)
        newslist = newsjson['result']['data']
        for news in newslist:
            post_url = news['url']
            # 转换成localtime
            time_local = time.localtime(int(news['ctime']))
            # 转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            meta = {
                'tag': tag,
                'title': news['title'],
                'pubtime': dt,
            }
            yield Request(post_url, callback=self.parsebody, meta=meta,dont_filter=True)

    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//div[@class='article']//p[position()>4]/text()").extract())
        item['pubtime'] = meta['pubtime']
        item['refer'] = '新浪新闻'
        yield item


