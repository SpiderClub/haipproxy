"""
python client for haipproxy
"""
import time
import threading

from ..utils import get_redis_conn
from ..config.rules import (
    SCORE_MAPS, TTL_MAPS,
    SPEED_MAPS)
from ..config.settings import (
    TTL_VALIDATED_RESOURCE, LONGEST_RESPONSE_TIME,
    LOWEST_SCORE, LOWEST_TOTAL_PROXIES,
    DATA_ALL)
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
    def __init__(self, usage, strategy='robin', fast_response=5,
                 score_map=SCORE_MAPS, ttl_map=TTL_MAPS, speed_map=SPEED_MAPS,
                 longest_response_time=LONGEST_RESPONSE_TIME, lowest_score=LOWEST_SCORE,
                 ttl_validated_resource=TTL_VALIDATED_RESOURCE, min_pool_size=LOWEST_TOTAL_PROXIES,
                 all_data=DATA_ALL, redis_args=None):
        """
        :param usage: one of SCORE_MAPS's keys, such as https
        :param strategy: the load balance of proxy ip, the value is
        one of ['robin', 'greedy']
        :param fast_response: if you use greedy strategy, it will be needed to
        decide whether a proxy ip should continue to be used
        :param score_map: score map of your project, default value is SCORE_MAPS in haipproxy.config.settings
        :param ttl_map: ttl map of your project, default value is TTL_MAPS in haipproxy.config.settings
        :param speed_map: speed map of your project, default value is SPEED_MAPS in haipproxy.config.settings
        :param ttl_validated_resource: time of latest validated proxies
        :param min_pool_size: min pool size of self.pool
        :param all_data: all proxies are stored in this set
        :param redis_args: redis connetion args, it's a dict, whose keys include host, port, db and password
        """
        # if there are multi parent classes, super is only used for the first parent according to MRO
        if usage not in score_map.keys():
            # client_logger.warning('task value is invalid, https task will be used')
            usage = 'https'
        score_queue = score_map.get(usage)
        ttl_queue = ttl_map.get(usage)
        speed_queue = speed_map.get(usage)
        super().__init__(score_queue, ttl_queue, speed_queue, longest_response_time,
                         lowest_score, ttl_validated_resource, min_pool_size)
        self.strategy = strategy
        # pool is a FIFO queue
        self.pool = list()
        self.min_pool_size = min_pool_size
        self.fast_response = fast_response
        self.all_data = all_data
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
        if len(self.pool) < self.min_pool_size:
            self.get_proxies()

    def delete_proxy(self, proxy):
        pipe = self.conn.pipeline()
        pipe.srem(self.all_data, proxy)
        pipe.zrem(self.score_queue, proxy)
        pipe.zrem(self.speed_queue, proxy)
        pipe.zrem(self.ttl_queue, proxy)
        pipe.execute()

    def _refresh_periodically(self):
        """refresh self.pool periodically, checking rate is 10 times/second"""
        while True:
            if len(self.pool) < int(2 * self.min_pool_size):
                self.get_proxies()
            time.sleep(0.2)
