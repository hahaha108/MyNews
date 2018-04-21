import json

from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
# from ..headers import qqheaders

class ifengnewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    name = 'ifengnews'
    redis_key = 'ifengnews:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('ifeng.com','news.ifeng.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(ifengnewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        baseurl = 'http://news.ifeng.com/hotnews/'
        yield Request(baseurl,callback=self.parsepage,dont_filter=True)


    def parsepage(self,response):
        sportslist = response.xpath("//div[@id='c06']/table/tr")[1:-1]
        entlist = response.xpath("//div[@id='c10']/table/tr")[1:-1]
        financelist = response.xpath("//div[@id='c07']/table/tr")[1:-1]

        for news in sportslist:
            url = news.xpath("./td/h3/a/@href").extract()[0]
            pubtime = news.xpath("./td[4]/text()").extract()
            if pubtime:
                pubtime = pubtime[0]
            else:
                pubtime = None
            meta = {
                'title':news.xpath("./td/h3/a/text()").extract()[0],
                'pubtime':pubtime,
                'tag':'sports'
            }
            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)

        for news in entlist:
            url = news.xpath("./td/h3/a/@href").extract()[0]
            pubtime = news.xpath("./td[4]/text()").extract()
            if pubtime:
                pubtime = pubtime[0]
            else:
                pubtime = None
            meta = {
                'title':news.xpath("./td/h3/a/text()").extract()[0],
                'pubtime':pubtime,
                'tag':'ent'
            }
            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)

        for news in financelist:
            url = news.xpath("./td/h3/a/@href").extract()[0]
            pubtime = news.xpath("./td[4]/text()").extract()
            if pubtime:
                pubtime = pubtime[0]
            else:
                pubtime = None
            meta = {
                'title':news.xpath("./td/h3/a/text()").extract()[0],
                'pubtime':pubtime,
                'tag':'finance'
            }
            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)


    def parsebody(self,response):
        meta = response.meta

        if not meta['pubtime']:
            pubtime = response.xpath("//div[@id='artical_sth']/p[@class='p_time']/span[1]/text()").extract()
            if pubtime:
                meta['pubtime'] = pubtime[0]
            else:
                meta['pubtime'] = None

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        item['pubtime'] = meta['pubtime']
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//div[@id='main_content']/p/text()").extract())
        item['refer'] = '凤凰新闻'
        if not item['body'] ==  '':
            yield item





