import ipaddress
import logging
import time
import uuid

import redis

from haipproxy.config.settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PIPE_BATCH_SIZE,
    LOCKER_PREFIX,
)

logger = logging.getLogger(__name__)

REDIS_POOL = None


#### redis ####
def get_redis_conn():
    global REDIS_POOL
    if REDIS_POOL == None:
        REDIS_POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    return redis.StrictRedis(connection_pool=REDIS_POOL)


def acquire_lock(conn, lock_name, acquire_timeout=10, lock_timeout=10):
    """inspired by the book 'redis in action' """
    identifier = str(uuid.uuid4())
    lock_name = LOCKER_PREFIX + lock_name
    end = time.time() + acquire_timeout

    while time.time() < end:
        if conn.set(lock_name, identifier, lock_timeout, nx=True):
            return identifier
        elif not conn.ttl(lock_name) or conn.ttl(lock_name) == -1:
            conn.expire(lock_name, lock_timeout)
        time.sleep(0.1)

    return False


def release_lock(conn, lock_name, identifier):
    pipe = conn.pipeline(True)
    lock_name = LOCKER_PREFIX + lock_name
    while True:
        try:
            pipe.watch(lock_name)
            identifier_origin = pipe.get(lock_name).decode()
            if identifier_origin == identifier:
                pipe.multi()
                pipe.delete(lock_name)
                pipe.execute()
                return True
            pipe.unwatch()
            break

        except redis.exceptions.WatchError:
            pass

    return False


class RedisOps(object):
    def __init__(self):
        self.redis_conn = get_redis_conn()
        self.rpipe = self.redis_conn.pipeline()
        self.rpipe_size = 0

    def flush(self):
        self.rpipe.execute()
        logger.info(f"{self.rpipe_size} redis commands executed")

    def set_proxy(self, proxy):
        if (
            not proxy
            or not is_valid_proxy(proxy=proxy)
            or self.redis_conn.exists(proxy)
        ):
            return
        self.rpipe.hmset(
            proxy,
            {
                "used_count": 0,
                "success_count": 0,
                "total_seconds": 0,
                "last_fail": "",
                "timestamp": 0,
                "score": 0,
            },
        )
        self.rpipe_size += 1
        if self.rpipe_size >= REDIS_PIPE_BATCH_SIZE:
            self.rpipe.execute()
            logger.info(f"{self.rpipe_size} redis commands executed")
            self.rpipe_size = 0

    def inc_stat(self, item):
        self.rpipe.hincrby(item["proxy"], "used_count")
        self.rpipe.hincrby(item["proxy"], "success_count", item["success"])
        self.rpipe.hincrby(item["proxy"], "total_seconds", item["seconds"])
        self.rpipe.hset(item["proxy"], "last_fail", item["fail"])
        if item["success"] != 0:
            self.rpipe.hset(item["proxy"], "timestamp", int(time.time()))
        self.rpipe.execute()


####
def is_valid_proxy(ip=None, port=None, protocol=None, proxy=None):
    if proxy:
        try:
            protocol, ip, port = proxy.split(":")
            ip = ip.lstrip("//")
        except ValueError as e:
            logger.warning(f"{proxy}: {e}")
            return False
    try:
        ipaddress.ip_address(ip)
        port = int(port)
    except ValueError as e:
        logger.warning(f"{ip}:{port} {e}")
        return False
    return (
        0 <= port
        and port <= 65535
        and protocol in ["http", "https", "sock4", "sock5", None]
    )
