import json
import re

from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
# from ..headers import qqheaders

class sohunewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    name = 'sohunews'
    redis_key = 'sohunews:start_urls'

    re_str1 = re.compile("item:\[(.*)\]")
    re_str2 = re.compile("\[(.*?),\"(.*?)\",\"(.*?)\",\"(.*?)\"]")

    # taglist = ['ent','sports','tech']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('sohu.com', 'news.sohu.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(sohunewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        sportsurl = 'http://sports.sohu.com/_scroll_newslist/20180420/news.inc'
        enturl = 'http://yule.sohu.com/_scroll_newslist/20180420/news.inc'
        yield Request(sportsurl,callback=self.parsepage1,meta={'tag':'sports'},dont_filter=True)
        yield Request(enturl, callback=self.parsepage1, meta={'tag': 'ent'}, dont_filter=True)

        techurl = "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=30&page=1&size=40"
        financeurl= "http://v2.sohu.com/public-api/feed?scene=CHANNEL&sceneId=15&page=1&size=40"
        yield Request(techurl,callback=self.parsepage2,meta={'tag':'tech'},dont_filter=True)
        yield Request(financeurl, callback=self.parsepage2, meta={'tag': 'finance'}, dont_filter=True)


    def parsepage1(self,response):
        tag = response.meta['tag']
        html = response.text
        # html = html.replace('var newsJason = ','')
        info = self.re_str1.findall(html)[0]
        # info = info.split(',')
        infolist = self.re_str2.findall(info)
        for info in infolist:
            url = info[2]
            meta = {
                'tag':tag,
                'title':info[1],
                'pubtime':info[3]
            }
            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)


    def parsepage2(self,response):
        tag = response.meta['tag']
        datalist = json.loads(response.text)
        for data in datalist:
            id = data['id']
            authorId = data['authorId']
            url = 'http://www.sohu.com/a/'+ str(id) +'_'+ str(authorId)
            title = data['title']

            meta = {
                'tag': tag,
                'title': title,
                'pubtime':None
            }
            yield Request(url, callback=self.parsebody, dont_filter=True, meta=meta)

    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        if not meta['pubtime']:
            pubtime = response.xpath("//div[@class='article-info']/span[@id='news-time']/text()")
            if pubtime:
                meta['pubtime'] = pubtime.extract()[0]
            else:
                meta['pubtime'] = None
        item['pubtime'] = meta['pubtime']
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//article[@id='mp-editor']/p/text()").extract())

        if not item['body'] ==  '':
            yield item





