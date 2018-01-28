"""
We use this validator to filter transparent ips, and give the ip resources a
initially score.
"""
import json

import requests


from ..redis_spiders import ValidatorRedisSpider
from .mixin import BaseSpider


class HttpBinValidator(BaseSpider, ValidatorRedisSpider):
    name = 'httpbin'
    urls = [
        'http://httpbin.org/ip',
        'https://httpbin.org/ip',
    ]

    def __init__(self):
        super().__init__()
        self.origin_ip = requests.get(self.urls[1]).json().get('origin')

    def parse_detail(self, response):
        ip = json.loads(response.body_as_unicode()).get('origin')
        # filter transparent ip resources
        if self.origin_ip in ip:
            return









