# -*- coding: utf-8 -*-


import json

from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
from ..headers import qqheaders
import requests
from lxml import etree

class EastmoneyNewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    '''
    start_url = "http://stock.eastmoney.com/news/cgszb.html"
    '''
    name = 'EastmoneyNews'
    redis_key = 'EastmoneyNews:start_urls'
    taglist = ['ent','sports','finance','tech']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('eastmoney.com', 'stock.eastmoney.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(EastmoneyNewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        # 取得总页数
        r = requests.get('http://stock.eastmoney.com/news/cgszb.html')
        html = etree.HTML(r.text)
        list = html.xpath("//div[@id='pagerNoDiv']//a/text()")
        page_total = int(list[-2])
        # 循环遍历所有页
        for i in range(1,page_total+1):
            # 得到每页的url
            url = 'http://stock.eastmoney.com/news/cgszb_'+str(i)+'.html'
            yield Request(url,callback=self.parsepage,dont_filter=True)

    def parsepage(self,response):
        # 得到新闻详情页的url列表
        post_url_list = response.xpath("//ul[@id='newsListContent']//p[@class='title']/a/@href").extract()
        # 遍历所有新闻url
        for post_url in post_url_list:
            yield Request(post_url, callback=self.parsebody, meta={'tag':'finance'},dont_filter=True)

    # 抽取页面数据
    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= response.xpath("//div[@class='main_left']//div[@class='newsContent']/h1/text()").extract()[0]
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//div[@class='newsContent']//div[@id='ContentBody']//p").xpath('string(.)').extract()).strip()
        item['pubtime'] = response.xpath("//div[@class='time-source']//div[@class='time']/text()").extract()[0]
        item['refer'] = '东方财富'
        yield item