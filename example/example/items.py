# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ExampleItem(Item):
    name = Field()
    description = Field()
    link = Field()
    crawled = Field()
    spider = Field()
    url = Field()

class LengzhishiItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = Field()
    crawled = Field()
    spider = Field()


class JdspiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    content = Field()
    url = Field()
    crawled = Field()
    spider = Field()


class LengzhishiLoader(ItemLoader):
    default_item_class = LengzhishiItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()

class ExampleLoader(ItemLoader):
    default_item_class = ExampleItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()
