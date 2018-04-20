import json
import re

import lxml
import lxml.etree
import requests


headers = {
'Host':'roll.news.qq.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Accept':'*/*',
'Referer':'http://www.qq.com/',
# 'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
}

response = requests.get('http://yule.sohu.com/_scroll_newslist/20180420/news.inc')
response.encoding = 'utf8'
html =response.text
# html = html.replace('var newsJason = ','')
re_str1 = re.compile("item:\[(.*)\]")
info = re_str1.findall(html)[0]
# info = info.split(',')
re_str2 = re.compile("\[(.*?),\"(.*?)\",\"(.*?)\",\"(.*?)\"]")
infolist = re_str2.findall(info)
for info in infolist:
    print(info[0])
    print(info[1])
    print(info[2])
    print(info[3])
# info = dict(html)
# print(info)
# info = json.loads(html)

# html = lxml.etree.HTML(response.text)
# print(response.text)
# info = html.xpath("//div[@id='c06']/table/tr")
# print(info)