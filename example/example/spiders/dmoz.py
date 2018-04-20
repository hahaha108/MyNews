from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import LengzhishiItem


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'dmoz'
    # allowed_domains = ['dmoz.org']
    # start_urls = ['http://www.dmoz.org/']
    #
    # rules = [
    #     Rule(LinkExtractor(
    #         restrict_css=('.top-cat', '.sub-cat', '.cat-item')
    #     ), callback='parse_directory', follow=True),
    # ]
    #
    # def parse_directory(self, response):
    #     for div in response.css('.title-and-desc'):
    #         yield {
    #             'name': div.css('.site-title::text').extract_first(),
    #             'description': div.css('.site-descr::text').extract_first().strip(),
    #             'link': div.css('a::attr(href)').extract_first(),
    #         }
    allowed_domains = ['lengdou.net']
    start_urls = ['http://lengdou.net/']

    linkextractor = LinkExtractor(allow=(r'/topic/\d+',))
    rules = [
        Rule(linkextractor,callback="parseContent",follow=True)
    ]

    def parseContent(self, response):
        content = response.xpath("//p[@class='topic-content']/text()").extract()[0]
        item = LengzhishiItem()
        item['content'] = content
        yield item
