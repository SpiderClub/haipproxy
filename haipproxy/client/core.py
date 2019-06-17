"""
This module provides core code for picking up proxies
"""
import time

# from logger import client_logger
from ..utils import decode_all


class IPFetcherMixin:
    def __init__(self, score_queue, ttl_queue, speed_queue,
                 longest_response_time, lowest_score, ttl_validated_resource,
                 min_pool_size):
        self.score_queue = score_queue
        self.ttl_queue = ttl_queue
        self.speed_queue = speed_queue
        self.longest_response_time = longest_response_time
        self.lowest_score = lowest_score
        self.ttl_validated_resource = ttl_validated_resource
        self.min_pool_size = min_pool_size

    def get_available_proxies(self, conn):
        """core algrithm to get proxies from redis"""
        start_time = int(time.time()) - self.ttl_validated_resource * 60
        pipe = conn.pipeline(False)
        pipe.zrevrangebyscore(self.score_queue, '+inf', self.lowest_score)
        pipe.zrevrangebyscore(self.ttl_queue, '+inf', start_time)
        pipe.zrangebyscore(self.speed_queue, 0,
                           1000 * self.longest_response_time)
        scored_proxies, ttl_proxies, speed_proxies = pipe.execute()
        scored_proxies, ttl_proxies, speed_proxies = set(scored_proxies), set(
            ttl_proxies), set(speed_proxies)

        proxies = scored_proxies & ttl_proxies & speed_proxies
        if not proxies or len(proxies) < self.min_pool_size * 2:
            proxies = ttl_proxies & speed_proxies
        if not proxies or len(proxies) < self.min_pool_size * 2:
            proxies = ttl_proxies | scored_proxies
        proxies = decode_all(proxies)

        return proxies
