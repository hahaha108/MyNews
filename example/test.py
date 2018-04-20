import redis

r = redis.Redis(host='10.36.131.52',port=6379)

r.set('name','value')
print(r.get('name'))