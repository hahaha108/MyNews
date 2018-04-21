import json

from scrapy_redis.spiders import RedisSpider
from MyNews.items import NewsItem
from scrapy import Request
from ..headers import qqheaders

class qqnewsSpider(RedisSpider):
    """Spider that reads urls from redis queue (qqnews:start_urls)."""

    '''
    start_url = "http://ent.qq.com/articleList/rolls/"
    '''
    name = 'qqnews'
    redis_key = 'qqnews:start_urls'
    taglist = ['ent','sports','finance','tech']

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('qq.com', 'news.qq.com')
        self.allowed_domains = filter(None, domain.split(','))
        super(qqnewsSpider, self).__init__(*args, **kwargs)

    def parse(self,response):
        for tag in self.taglist:
            url = 'http://roll.news.qq.com/interface/cpcroll.php?site='+tag+'&mode=1&cata=&date=2018-04-20&page=1'
            yield Request(url,callback=self.parsepage,headers=qqheaders,meta={'tag':tag},dont_filter=True)

    def parsepage(self,response):
        tag = response.meta['tag']
        newsjson = json.loads(response.text)
        newslist = newsjson['data']['article_info']
        for news in newslist:
            url = news['url']
            meta = {
                'tag':tag,
                'title':news['title'],
                'pubtime':news['time'],
            }
            yield Request(url,callback=self.parsebody,dont_filter=True,meta=meta)


    def parsebody(self,response):
        meta = response.meta

        item = NewsItem()
        item['tag'] = meta['tag']
        item['title']= meta['title']
        item['url'] = response.url
        item['body'] = '\n'.join(response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@class='text']/text()").extract())
        item['pubtime'] = meta['pubtime']
        item['refer'] = '腾讯新闻'
        if not item['body'] ==  '':
            yield item





