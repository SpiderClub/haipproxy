"""
This module provides core code for picking up proxies
"""
import time

from ..utils import decode_all


class IPFetcherMixin:
    def __init__(self,
                 longest_response_time, lowest_score, ttl_validated_resource,
                 min_pool_size):
        self.longest_response_time = longest_response_time
        self.lowest_score = lowest_score
        self.min_pool_size = min_pool_size

    def get_available_proxies(self, conn):
        """core algrithm to get proxies from redis"""
        start_time = int(time.time()) - 2 * 60
        pipe = conn.pipeline(False)
        proxies = decode_all(proxies)

        return proxies
