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

response = requests.get('http://news.163.com/special/0001386F/rank_tech.html')
html = lxml.etree.HTML(response.text)
print(response.text)
info = html.xpath("//div[@class='tabContents active']/table/tr/td/a")
print(info)