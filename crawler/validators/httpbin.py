"""
We use this validator to filter transparent ips, and give the ip resources a
initially score.
"""
import time
import json
from json.decoder import JSONDecodeError

import requests

from config.rules import (
    SPEED_MAPS, TTL_MAPS,
    SCORE_MAPS)
from config.settings import (
    INIT_HTTP_QUEUE, TEMP_HTTP_QUEUE,
    TEMP_HTTPS_QUEUE, VALIDATED_HTTP_QUEUE,
    VALIDATED_HTTPS_QUEUE, TTL_HTTP_QUEUE,
    TTL_HTTPS_QUEUE, SPEED_HTTP_QUEUE,
    SPEED_HTTPS_QUEUE)
from ..redis_spiders import ValidatorRedisSpider
from ..items import (
    ProxyScoreItem, ProxyVerifiedTimeItem,
    ProxySpeedItem)
from .base import BaseValidator


class HttpBinInitValidator(BaseValidator, ValidatorRedisSpider):
    """This validator do initially work for ip resources"""
    name = 'init'
    urls = [
        'http://httpbin.org/ip',
        'https://httpbin.org/ip',
    ]
    task_queue = INIT_HTTP_QUEUE
    https_tasks = ['https', 'weibo']
    http_tasks = ['http']

    def __init__(self):
        super().__init__()
        self.origin_ip = requests.get(self.urls[1]).json().get('origin')

    def is_transparent(self, response):
        """filter transparent ip resources"""
        if not response.body_as_unicode():
            return True
        try:
            ip = json.loads(response.body_as_unicode()).get('origin')
            if self.origin_ip in ip:
                return True
        except (AttributeError, JSONDecodeError):
            return True

        return False

    def set_item_queue(self, url, proxy, score, incr, speed=0):
        items = list()
        tasks = self.https_tasks if 'https' in url else self.http_tasks
        for task in tasks:
            score_item = ProxyScoreItem(url=proxy, score=score, incr=incr)
            ttl_item = ProxyVerifiedTimeItem(url=proxy, verified_time=int(time.time()), incr=incr)
            speed_item = ProxySpeedItem(url=proxy, response_time=speed, incr=incr)
            score_item['queue'] = SCORE_MAPS.get(task)
            ttl_item['queue'] = TTL_MAPS.get(task)
            speed_item['queue'] = SPEED_MAPS.get(task)
            items.append(score_item)
            items.append(ttl_item)
            items.append(speed_item)
        return items


class HttpValidator(BaseValidator, ValidatorRedisSpider):
    """This validator check the liveness of http proxy resources"""
    name = 'http'
    urls = [
        'http://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTP_QUEUE
    score_queue = VALIDATED_HTTP_QUEUE
    ttl_queue = TTL_HTTP_QUEUE
    speed_queue = SPEED_HTTP_QUEUE


class HttpsValidator(BaseValidator, ValidatorRedisSpider):
    """This validator check the liveness of https proxy resources"""
    name = 'https'
    urls = [
        'https://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTPS_QUEUE
    score_queue = VALIDATED_HTTPS_QUEUE
    ttl_queue = TTL_HTTPS_QUEUE
    speed_queue = SPEED_HTTPS_QUEUE















