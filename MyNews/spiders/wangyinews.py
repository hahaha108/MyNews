import json

from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
# from ..headers import qqheaders

class wangyinewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    '''
    start_url = "http://ent.qq.com/articleList/rolls/"
    '''
    name = 'wangyinews'
    redis_key = 'wangyinews:start_urls'
    taglist = ['ent','sports','tech']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('163.com', 'news.163.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(wangyinewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        monenyurl = 'http://money.163.com/special/002526BH/rank.html'
        yield Request(monenyurl,callback=self.parsepage,meta={'tag':'finance'},dont_filter=True)

        for tag in self.taglist:
            url = 'http://news.163.com/special/0001386F/rank_'+tag+'.html'
            yield Request(url,callback=self.parsepage,meta={'tag':tag},dont_filter=True)

    def parsepage(self,response):

        tag = response.meta['tag']
        # newsjson = json.loads(response.text)
        newslist = response.xpath("//div[@class='tabContents active']/table/tr/td/a")
        for news in newslist:
            url = news.xpath("./@href").extract()[0]
            meta = {
                'tag':tag,
                'title':news.xpath("./text()").extract()[0],
            }


            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)


    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//div[@id='epContentLeft']/div[@class='post_body']/div[@id='endText']/p/text()").extract())
        pubtime = response.xpath("//div[@id='epContentLeft']/div[@class='post_time_source']/text()[1]").extract()
        if pubtime:
            item['pubtime'] = pubtime[0]
        else:
            item['pubtime'] = None
        if not item['body'] ==  '':
            yield item





