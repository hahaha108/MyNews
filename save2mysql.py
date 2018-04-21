import json

import pymysql
import redis
import time


def saveitem(r,conn,item):
    if r.llen(item) > 0:
        source, data = r.blpop(item)
        item = json.loads(data)
        try:
            with conn.cursor() as cur:
                cur.execute( r'''
                insert into mynews (title,pubtime,url,tag,refer,body) 
                VALUES ('%s','%s','%s','%s','%s','%s')'''%(item['title'],item['pubtime'],item['url'],item['tag'],item['refer'],item['body']))
                conn.commit()
                print("inserted %s" % item['title'])
        except Exception as e:
            print(e)
    else:
        pass



conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='123456',database='news',charset='utf8')

r = redis.Redis(host='10.36.131.52',port=6379)



sql = '''
drop table if exists mynews;
'''
with conn.cursor() as cur:
    cur.execute(sql)
    conn.commit()

sql = '''
create table mynews(
id int PRIMARY KEY not null AUTO_INCREMENT,  
title VARCHAR(200),
pubtime VARCHAR(130),
body Text,
url VARCHAR(250),
tag VARCHAR(30),
refer VARCHAR(30)
);
'''

with conn.cursor() as cur:
    cur.execute(sql)
    conn.commit()

conn.close()

while True:
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='news', charset='utf8')
    saveitem(r, conn, 'qqnews:items')
    saveitem(r, conn, 'ifengnews:items')
    saveitem(r, conn, 'sohunews:items')
    saveitem(r, conn, 'wangyinews:items')
    conn.close()


