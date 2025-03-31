import redis

from test_task_pesk.settings import REDIS_URL

redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
