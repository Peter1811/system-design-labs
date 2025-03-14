import redis

# redis = redis.Redis(host='redis', port=6379)

REDIS_URL = 'redis://redis:6379'

def get_redis():
    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield client
    
    finally:
        client.close()