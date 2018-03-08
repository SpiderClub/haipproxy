"""
This module privodes core algrithm to pick up proxy ip resources.
"""
import time

# from logger import client_logger
from utils import (
    get_redis_conn, decode_all)
from config.rules import (
    SCORE_MAPS, TTL_MAPS,
    SPEED_MAPS)
from config.settings import (
    TTL_VALIDATED_RESOURCE, LONGEST_RESPONSE_TIME,
    LOWEST_SCORE, DATA_ALL)


class Strategy:
    strategy = None

    def check(self, strategy):
        return self.strategy == strategy

    def get_proxies_by_stragery(self, pool):
        raise NotImplementedError


class RobinStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.strategy = 'robin'

    def get_proxies_by_stragery(self, pool):
        if not pool:
            return None
        proxy = pool[0]
        pool[0], pool[-1] = pool[-1], pool[0]
        return proxy


class GreedyStrategy(Strategy):
    def __init__(self):
        self.strategy = 'greedy'

    def get_proxies_by_stragery(self, pool):
        if not pool:
            return None
        return pool[0]


class ProxyFetcher:
    def __init__(self, usage, strategy='robin', length=10,
                 fast_response=5, redis_args=None):
        """
        :param usage: one of SCORE_MAPS's keys, such as https
        :param length: if total available proxies are less than length,
        you must refresh pool
        :param strategy: the load balance of proxy ip, the value is
        one of ['robin', 'greedy']
        :param fast_response: if you use greedy strategy, if will be needed to
        decide whether a proxy ip should continue to be used
        :param redis_args: redis connetion args, it's a dict, the keys include host, port, db and password
        """
        self.score_queue = SCORE_MAPS.get(usage)
        self.ttl_queue = TTL_MAPS.get(usage)
        self.speed_queue = SPEED_MAPS.get(usage)
        self.strategy = strategy
        # pool is a queue, which is FIFO
        self.pool = list()
        self.length = length
        self.fast_response = fast_response
        self.handlers = [RobinStrategy(), GreedyStrategy()]
        if isinstance(redis_args, dict):
            self.conn = get_redis_conn(**redis_args)
        else:
            self.conn = get_redis_conn()

    def get_proxy(self):
        """
        get one available proxy from redis, if not any, None is returned
        :return:
        """
        # todo consider aysnc or multi thread
        proxy = None
        self.refresh()
        for handler in self.handlers:
            if handler.strategy == self.strategy:
                proxy = handler.get_proxies_by_stragery(self.pool)
        return proxy

    def get_proxies(self):
        """core algrithm to get proxies from redis"""
        start_time = int(time.time()) - TTL_VALIDATED_RESOURCE * 60

        pipe = self.conn.pipeline(False)
        pipe.zrevrangebyscore(self.score_queue, '+inf', LOWEST_SCORE)
        pipe.zrevrangebyscore(self.ttl_queue, '+inf', start_time)
        pipe.zrangebyscore(self.speed_queue, 0, 1000*LONGEST_RESPONSE_TIME)
        scored_proxies, ttl_proxies, speed_proxies = pipe.execute()
        proxies = scored_proxies and ttl_proxies and speed_proxies
        if not proxies or len(proxies) < self.length*2:
            proxies = (ttl_proxies and speed_proxies) or scored_proxies

        if not proxies or len(proxies) < self.length*2:
            proxies = ttl_proxies or scored_proxies
        proxies = decode_all(proxies)
        # client_logger.info('{} proxies have been fetched'.format(len(proxies)))
        print('{} proxies have been fetched'.format(len(proxies)))
        self.pool.extend(proxies)
        return self.pool

    def proxy_feedback(self, res, response_time=None):
        """
        client should give feedbacks after executing get_proxy()
        :param res: one value of ['success', 'failure']
        :param response_time: the response time using current proxy ip
        """
        if res == 'failure':
            self.delete_proxy(self.pool[0])
            return

        # prevent from using proxy with slow speed always
        if self.strategy == 'greedy' and self.fast_response*1000 < response_time:
            self.pool[0], self.pool[-1] = self.pool[-1], self.pool[0]

    def refresh(self):
        if len(self.pool) < self.length:
            self.get_proxies()

    def delete_proxy(self, proxy):
        # it's not thread safe
        self.pool.pop(0)
        pipe = self.conn.pipeline(True)
        pipe.srem(DATA_ALL, proxy)
        pipe.zrem(self.score_queue, proxy)
        pipe.zrem(self.speed_queue, proxy)
        pipe.zrem(self.ttl_queue, proxy)
        pipe.execute()
