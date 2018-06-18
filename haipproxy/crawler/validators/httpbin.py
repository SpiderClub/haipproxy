"""
We use this validator to filter transparent ips, and give the ip resources an
initial score.
"""
import time
import json
from json.decoder import JSONDecodeError

import requests

from haipproxy.config.rules import (
    SPEED_MAPS, TTL_MAPS,
    SCORE_MAPS, HTTP_TASKS,
    HTTPS_TASKS)
from haipproxy.config.settings import (
    INIT_HTTP_QUEUE, TEMP_HTTP_QUEUE,
    TEMP_HTTPS_QUEUE, VALIDATED_HTTP_QUEUE,
    VALIDATED_HTTPS_QUEUE, TTL_HTTP_QUEUE,
    TTL_HTTPS_QUEUE, SPEED_HTTP_QUEUE,
    SPEED_HTTPS_QUEUE, ORIGIN_IP)
from ..redis_spiders import ValidatorRedisSpider
from ..items import (
    ProxyScoreItem, ProxyVerifiedTimeItem,
    ProxySpeedItem)
from .base import BaseValidator


class HttpBinInitValidator(BaseValidator, ValidatorRedisSpider):
    """This validator does initial work for ip resources.
    　　It will filter transparent ip and store proxies in http_task
       and https_tasks
    """
    name = 'init'
    urls = [
        'http://httpbin.org/ip',
        'https://httpbin.org/ip',
    ]
    use_set = False
    task_queue = INIT_HTTP_QUEUE
    # https_tasks = ['https']
    # distribute proxies to each queue, according to
    # VALIDORTOR_TASKS in rules.py
    https_tasks = HTTPS_TASKS
    http_tasks = HTTP_TASKS

    def __init__(self):
        super().__init__()
        if ORIGIN_IP:
            self.origin_ip = ORIGIN_IP
        else:
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
        # todo set proxy to tmp_queue
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
    """This validator checks the liveness of http proxy resources"""
    name = 'http'
    urls = [
        'http://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTP_QUEUE
    score_queue = VALIDATED_HTTP_QUEUE
    ttl_queue = TTL_HTTP_QUEUE
    speed_queue = SPEED_HTTP_QUEUE


class HttpsValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of https proxy resources"""
    name = 'https'
    urls = [
        'https://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTPS_QUEUE
    score_queue = VALIDATED_HTTPS_QUEUE
    ttl_queue = TTL_HTTPS_QUEUE
    speed_queue = SPEED_HTTPS_QUEUE
