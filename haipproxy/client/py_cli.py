"""
python client for haipproxy
"""
import logging
import threading
import time

from ..utils import get_redis_conn
from ..config.settings import (LONGEST_RESPONSE_TIME,
                               LOWEST_SCORE, LOWEST_TOTAL_PROXIES, DATA_ALL)
from .core import IPFetcherMixin

lock = threading.RLock()

logger = logging.getLogger(__name__)


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
    def __init__(self,
                 usage,
                 strategy='robin',
                 fast_response=5,
                 longest_response_time=LONGEST_RESPONSE_TIME,
                 lowest_score=LOWEST_SCORE,
                 min_pool_size=LOWEST_TOTAL_PROXIES,
                 all_data=DATA_ALL):
        """
        :param usage: one of SCORE_QUEUE_MAPS's keys, such as https
        :param strategy: the load balance of proxy ip, the value is
        one of ['robin', 'greedy']
        :param fast_response: if you use greedy strategy, it will be needed to
        decide whether a proxy ip should continue to be used
        :param ttl_validated_resource: time of latest validated proxies
        :param min_pool_size: min pool size of self.pool
        :param all_data: all proxies are stored in this set
        :param redis_args: redis connetion args, it's a dict, whose keys include host, port, db and password
        """
        # if there are multi parent classes, super is only used for the first parent according to MRO
        if usage not in score_map.keys():
            # client_logger.warning('task value is invalid, https task will be used')
            usage = 'https'
        super().__init__(
                         longest_response_time, lowest_score,
                         min_pool_size)
        self.strategy = strategy
        # pool is a FIFO queue
        self.pool = list()
        self.min_pool_size = min_pool_size
        self.fast_response = fast_response
        self.all_data = all_data
        self.handlers = [RobinStrategy(), GreedyStrategy()]
        self.redis_conn = get_redis_conn()
        t = threading.Thread(target=self._refresh_periodically)
        t.setDaemon(True)
        t.start()

    def get_proxy(self):
        """
        get one available proxy from redis, if there's none, None is returned
        """
        proxy = None
        self.refresh()
        for handler in self.handlers:
            if handler.strategy == self.strategy:
                proxy = handler.get_proxies_by_stragery(self.pool)
        return proxy

    def get_proxies(self):
        # the older proxies will not be dropped
        proxies = self.get_available_proxies(self.redis_conn)
        logger.info('{} proxies have been fetched'.format(len(proxies)))
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
                handler.process_feedback(self.pool,
                                         res,
                                         proxy,
                                         real=response_time,
                                         expected=self.fast_response)

    def refresh(self):
        if len(self.pool) < self.min_pool_size:
            self.get_proxies()

    def delete_proxy(self, proxy):
        pipe = self.redis_conn.pipeline()
        pipe.srem(self.all_data, proxy)
        pipe.execute()

    def _refresh_periodically(self):
        """refresh self.pool periodically, checking rate is 10 times/second"""
        while True:
            if len(self.pool) < int(2 * self.min_pool_size):
                self.get_proxies()
            time.sleep(0.2)
