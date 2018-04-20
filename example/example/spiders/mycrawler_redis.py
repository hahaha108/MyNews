import re

import lxml
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider, RedisMixin
from example.items import LengzhishiItem, JdspiderItem
from scrapy.spiders import CrawlSpider
import requests


class MyCrawler(RedisCrawlSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'mycrawler_redis'
    redis_key = 'mycrawler:start_urls'

    # rules = (
    #     # follow all links
    #     Rule(LinkExtractor(), callback='parse_page', follow=True),
    # )
    #
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(MyCrawler, self).__init__(*args, **kwargs)
    #
    # def parse_page(self, response):
    #     return {
    #         'name': response.css('title::text').extract_first(),
    #         'url': response.url,
    #     }

    rules = [
        Rule(LinkExtractor(allow=(r'jd\.com/\d+\.html',)),callback="parseContent",follow=True)
    ]


    def set_crawler(self, crawer):
        CrawlSpider.set_crawler(self, crawer)  # 设置默认爬去
        RedisMixin.setup_redis(self)  # url由redis

    def parseContent(self, response):
        # content = response.xpath("//p[@class='topic-content']/text()").extract()[0]
        # item = LengzhishiItem()
        # item['content'] = content
        # yield item
        # return {
        #          'content': response.xpath("//p[@class='topic-content']/text()").extract()[0],
        #          'url': response.url,
        #      }
        namelist = []
        contentlist = []

        item = JdspiderItem()
        url = response.url
        response = requests.get(url)

        html = lxml.etree.HTML(response.text)

        infolist = html.xpath("//*[@id=\"detail\"]/div[2]/div//dl")

        name = html.xpath("//div[@class='item ellipsis']/text()")[0].strip()

        # print("商品名称：", name)
        namelist.append("商品名称")
        contentlist.append(name)
        # item['name'] = name

        try:
            baozhuang = html.xpath("//div[@class='package-list']/p/text()")[0].strip().replace("\n", '、')
        except:
            baozhuang = "未列明"
        # print("包装清单：", baozhuang)
        namelist.append("包装清单")
        contentlist.append(baozhuang)

        # jieshao = html.xpath("//div[@class='item hide']/text()")[0]
        # print("商品简介：",jieshao)

        # 京东的价格采用ajax动态加载，而且同一IP请求过于频繁可能触发验证码，这里很坑
        # 如果触发验证码则获取不到价格信息，暂时没找到好的解决办法，添加异常处理
        try:
            number = re.findall(r"com/(\d+)\.html", url)[0]
            # print(number)

            ajaxUrl = r"https://p.3.cn/prices/mgets?pdtk=&skuIds=J_" + number

            ajaxResponse = requests.get(ajaxUrl)
            # print(ajaxResponse.text)
            prices = re.findall('"p":"(.*?)"', ajaxResponse.text)[0].strip()
            # print("价格：", prices)

        except:
            prices = "获取失败"

        namelist.append("价格")
        contentlist.append(prices)

        for info in infolist:
            titles = info.xpath("./dt/text()")
            contents = info.xpath("./dd/text()")
            for title, content in zip(titles, contents):
                # print(title, ':', content)
                namelist.append(title.strip())
                contentlist.append(content.strip())

        item['name'] = namelist
        item['content'] = contentlist
        item['url'] = response.url

        yield item