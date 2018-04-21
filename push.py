import redis


r = redis.Redis(host='10.36.131.52',port=6379)

r.lpush('qqnews:start_urls','https://news.qq.com')
r.lpush('wangyinews:start_urls','https://news.163.com')
r.lpush('ifengnews:start_urls','https://news.ifeng.com')
r.lpush('sohunews:start_urls','https://news.sohu.com')