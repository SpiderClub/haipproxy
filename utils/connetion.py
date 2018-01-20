import redis

from config.settings import (
    REDIS_HOST, REDIS_PORT, DEFAULT_REDIS_DB, REDIS_PASSWORD)


def get_redis_con(**kwargs):
    host = kwargs.get('host', REDIS_HOST)
    port = kwargs.get('port', REDIS_PORT)
    db = kwargs.get('db', DEFAULT_REDIS_DB)
    password = kwargs.get('password', REDIS_PASSWORD)
    return redis.StrictRedis(host, port, db, password)