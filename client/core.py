"""
This module provides core code for picking up proxies
"""
import time

# from logger import client_logger
from utils import decode_all
from config.rules import (
    SCORE_MAPS, TTL_MAPS,
    SPEED_MAPS)
from config.settings import (
    TTL_VALIDATED_RESOURCE, LONGEST_RESPONSE_TIME,
    LOWEST_SCORE, LOWEST_TOTAL_PROXIES)


class IPFetcherMixin:
    def __init__(self, usage):
        if usage not in SCORE_MAPS.keys():
            # client_logger.warning('task value is invalid, https task will be used')
            usage = 'https'
        self.score_queue = SCORE_MAPS.get(usage)
        self.ttl_queue = TTL_MAPS.get(usage)
        self.speed_queue = SPEED_MAPS.get(usage)

    def get_available_proxies(self, conn):
        """core algrithm to get proxies from redis"""
        start_time = int(time.time()) - TTL_VALIDATED_RESOURCE * 60
        pipe = conn.pipeline(False)
        pipe.zrevrangebyscore(self.score_queue, '+inf', LOWEST_SCORE)
        pipe.zrevrangebyscore(self.ttl_queue, '+inf', start_time)
        pipe.zrangebyscore(self.speed_queue, 0, 1000 * LONGEST_RESPONSE_TIME)
        scored_proxies, ttl_proxies, speed_proxies = pipe.execute()
        scored_proxies, ttl_proxies, speed_proxies = set(scored_proxies), set(ttl_proxies), set(speed_proxies)

        proxies = scored_proxies & ttl_proxies & speed_proxies
        if not proxies or len(proxies) < LOWEST_TOTAL_PROXIES * 2:
            proxies = ttl_proxies & speed_proxies
        if not proxies or len(proxies) < LOWEST_TOTAL_PROXIES * 2:
            proxies = ttl_proxies | scored_proxies
        proxies = decode_all(proxies)

        return proxies
