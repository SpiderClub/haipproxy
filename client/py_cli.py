"""
This module provides core algrithm to pick up proxy ip resources.
"""
import time
import threading

from utils import get_redis_conn
from config.settings import (
    DATA_ALL, LOWEST_TOTAL_PROXIES)
from .core import IPFetcherMixin

__all__ = ['ProxyFetcher']

lock = threading.RLock()


class Strategy:
    strategy = None

    def check(self, strategy):
        return self.strategy == strategy

    def get_proxies_by_stragery(self, pool):
        """
        :param pool: pool is a list, which is mutable
        :return:
        """
        raise NotImplementedError

    def process_feedback(self, pool, res, proxy, **kwargs):
        """
        :param pool: ProxyFetcher's pool
        :param res: success or failure
        :param proxy: proxy ip
        :param kwargs: response time or expected response time
        :return: None
        """
        raise NotImplementedError


class RobinStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.strategy = 'robin'

    def get_proxies_by_stragery(self, pool):
        if not pool:
            return None

        proxy = pool.pop(0)
        pool.append(proxy)
        return proxy

    def process_feedback(self, pool, res, proxy, **kwargs):
        if res == 'failure':
            if pool[-1] == proxy:
                with lock:
                    if pool[-1] == proxy:
                        pool.pop()
        return


class GreedyStrategy(Strategy):
    def __init__(self):
        self.strategy = 'greedy'

    def get_proxies_by_stragery(self, pool):
        if not pool:
            return None
        return pool[0]

    def process_feedback(self, pool, res, proxy, **kwargs):
        if res == 'failure':
            if pool[0] == proxy:
                with lock:
                    if pool[0] == proxy:
                        pool.pop(0)
            return
        expected_time = kwargs.get('expected')
        real_time = kwargs.get('real')
        if expected_time * 1000 < real_time:
            pool.pop(0)
            pool.append(proxy)


class ProxyFetcher(IPFetcherMixin):
    def __init__(self, usage, strategy='robin', fast_response=5, redis_args=None):
        """
        :param usage: one of SCORE_MAPS's keys, such as https
        you must refresh pool
        :param strategy: the load balance of proxy ip, the value is
        one of ['robin', 'greedy']
        :param fast_response: if you use greedy strategy, it will be needed to
        decide whether a proxy ip should continue to be used
        :param redis_args: redis connetion args, it's a dict, whose keys
        include host, port, db and password
        """
        # if there are multi parent classes, super is only used for the first parent according to MRO
        super().__init__(usage)
        self.strategy = strategy
        # pool is a queue, which is FIFO
        self.pool = list()
        self.fast_response = fast_response
        self.handlers = [RobinStrategy(), GreedyStrategy()]
        if isinstance(redis_args, dict):
            self.conn = get_redis_conn(**redis_args)
        else:
            self.conn = get_redis_conn()
        t = threading.Thread(target=self._refresh_periodically)
        t.setDaemon(True)
        t.start()

    def get_proxy(self):
        """
        get one available proxy from redis, if there's none, None is returned
        :return:
        """
        proxy = None
        self.refresh()
        for handler in self.handlers:
            if handler.strategy == self.strategy:
                proxy = handler.get_proxies_by_stragery(self.pool)
        return proxy

    def get_proxies(self):
        # the older proxies will not be dropped
        proxies = self.get_available_proxies(self.conn)
        # client_logger.info('{} proxies have been fetched'.format(len(proxies)))
        print('{} proxies have been fetched'.format(len(proxies)))
        self.pool.extend(proxies)
        return self.pool

    def proxy_feedback(self, res, proxy, response_time=None):
        """
        client should give feedbacks after executing get_proxy()
        :param res: value of 'success' or 'failure'
        :param proxy: proxy ip
        :param response_time: the response time using current proxy ip
        """
        for handler in self.handlers:
            if handler.strategy == self.strategy:
                handler.process_feedback(self.pool, res,
                                         proxy, real=response_time,
                                         expected=self.fast_response)

    def refresh(self):
        if len(self.pool) < LOWEST_TOTAL_PROXIES:
            self.get_proxies()

    def delete_proxy(self, proxy):
        pipe = self.conn.pipeline(True)
        pipe.srem(DATA_ALL, proxy)
        pipe.zrem(self.score_queue, proxy)
        pipe.zrem(self.speed_queue, proxy)
        pipe.zrem(self.ttl_queue, proxy)
        pipe.execute()

    def _refresh_periodically(self):
        """refresh self.pool periodically, checking rate is 10 times/second"""
        while True:
            if len(self.pool) < int(2 * LOWEST_TOTAL_PROXIES):
                self.get_proxies()
            time.sleep(0.2)
