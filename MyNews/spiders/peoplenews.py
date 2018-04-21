# -*- coding: utf-8 -*-
import json
import time
from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
from ..headers import qqheaders

class PeopleNewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    '''
    start_url = "http://news.people.com.cn/"
    '''
    name = 'peoplenews'
    redis_key = 'peoplenews:start_urls'
    tags_list = ['ent','sports','finance','tech']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('people.com.cn', 'news.people.com.cn')
        self.allowed_domains = filter(None, domain.split(','))
        super(PeopleNewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        # 获取总页数:
        # page_total = int(response.xpath('//div[@id="Pagination"]//span[last()-1]').extract())
        # 获取当前时间戳
        now = int(time.time())
        url = 'http://news.people.com.cn/210801/211150/index.js?_='+str(now)
        yield Request(url, callback=self.parsepage_url, dont_filter=True)


    def parsepage_url(self,response):
        newsjson = json.loads(response.text)
        newslist = newsjson['items']
        for news in newslist:
            post_title = news['title']
            pub_time = news['date']
            post_url = news['url']
            if 'ent' in post_url:
                yield Request(post_url, callback=self.parsebody, meta={'tag':'ent','title':post_title,'pubtime':pub_time},dont_filter=True)
            if 'sports' in post_url:
                yield Request(post_url, callback=self.parsebody, meta={'tag':'sport','title':post_title,'pubtime':pub_time},dont_filter=True)
            if 'finance' in post_url:
                yield Request(post_url, callback=self.parsebody, meta={'tag':'finance','title':post_title,'pubtime':pub_time},dont_filter=True)
            if 'it' in post_url:
                yield Request(post_url, callback=self.parsebody, meta={'tag':'tech','title':post_title,'pubtime':pub_time},dont_filter=True)


    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        item['url'] = response.url
        item['body'] = ''.join(response.xpath('//div[@class="fl text_con_left"]//div[@id="rwb_zw"]//p/text()').extract()).replace('\t','')
        item['pubtime'] = meta['pubtime']
        item['refer'] = '人民网'
        yield item


