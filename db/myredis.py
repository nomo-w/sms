import redis
from config import RedisSql


class RedisClient(redis.StrictRedis):
    '''单例模式'''
    _instance = {}

    def __init__(self, server):
        redis.StrictRedis.__init__(self, **server)

    def __new__(cls, *args):
        if str(args) not in cls._instance:
            cls._instance[str(args)] = super(RedisClient, cls).__new__(cls)
        return cls._instance[str(args)]


def mdelete(key):
    return db_redis.delete(key)


def mpush(data, key):
    '''存入消息队列'''
    return db_redis.lpush(key, data)


def mpop(key):
    '''从消息队列中取, 移除并返回列表的第一个元素'''
    return db_redis.rpop(key)


def mlen(key):
    return db_redis.llen(key)


def mpipeline():
    return db_redis.pipeline()


def mset(key, data, timeout=None):
    if timeout is None:
        return db_redis.set(key, data)
    else:
        return db_redis.setex(key, timeout, data)


def mget(key):
    data = db_redis.get(key)
    return data.decode('utf8') if data is not None else data


db_redis = RedisClient({'host': RedisSql.host, 'port': RedisSql.port, 'db': RedisSql.db})

