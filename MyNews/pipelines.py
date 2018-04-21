# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime


class MynewsPipeline(object):
    def process_item(self, item, spider):
        item["crawled"] = datetime.utcnow()
        item["spider"] = spider.name
        item["body"] = item["body"].strip()
        item["pubtime"] = item["pubtime"].replace('来源: ','')
        item["pubtime"] = item["pubtime"].strip()
        return item
