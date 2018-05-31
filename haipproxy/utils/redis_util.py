import uuid
import time

import redis

from haipproxy.config.settings import (
    REDIS_HOST, REDIS_PORT, DEFAULT_REDIS_DB,
    REDIS_PASSWORD, LOCKER_PREFIX)


def get_redis_conn(**kwargs):
    host = kwargs.get('host', REDIS_HOST)
    port = kwargs.get('port', REDIS_PORT)
    db = kwargs.get('db', DEFAULT_REDIS_DB)
    password = kwargs.get('password', REDIS_PASSWORD)
    return redis.StrictRedis(host, port, db, password)


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
