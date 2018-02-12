"""
We use this validator to filter transparent ips, and give the ip resources a
initially score.
"""
import json

import requests

from config.settings import (
    INIT_HTTP_QUEUE, VALIDATOR_HTTP_TASK, VALIDATOR_HTTPS_TASK)
from ..redis_spiders import ValidatorRedisSpider
from .mixin import BaseValidator


class HttpBinInitValidator(BaseValidator, ValidatorRedisSpider):
    """This validator do initially work for ip resources"""
    name = 'init'
    task_types = [INIT_HTTP_QUEUE]
    urls = [
        'http://httpbin.org/ip',
        'https://httpbin.org/ip',
    ]

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
        except AttributeError:
            return True

        return False


class CommonValidator(BaseValidator, ValidatorRedisSpider):
    """This validator check the liveness of ip resources"""
    name = 'common'
    urls = [
        'http://httpbin.org/ip',
        'https://httpbin.org/ip',
    ]
    task_types = [VALIDATOR_HTTP_TASK, VALIDATOR_HTTPS_TASK]













