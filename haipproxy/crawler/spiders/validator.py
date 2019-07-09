import json
import requests
import sys

from json.decoder import JSONDecodeError
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (DNSLookupError, ConnectionRefusedError,
                                    TimeoutError, TCPTimedOutError)

from .redis_spiders import RedisSpider
from haipproxy.crawler.items import ProxyStatInc


class BaseValidator(RedisSpider):
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'RETRY_ENABLED': False,
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyStatPipeline': 200,
        }
    }
    success_key = ''

    def start_requests(self):
        for proxy in self.redis_conn.scan_iter(match='*://*'):
            proxy = proxy.decode()
            req = Request(self.get_url(proxy),
                          meta={'proxy': proxy},
                          callback=self.parse,
                          errback=self.parse_error)
            yield req

    def parse(self, response):
        proxy = response.meta.get('proxy')
        seconds = int(response.meta.get('download_latency'))
        success = 1
        fail = ''
        if not self.is_ok(response):
            success = 0
            fail = 'badcontent'
            self.logger.error(f'{proxy} got wrong content')
        else:
            self.logger.info(f'good ip {proxy}')
        yield ProxyStatInc(proxy=proxy,
                           success=success,
                           seconds=seconds,
                           fail=fail)

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        self.logger.warning(f'proxy {proxy} has failed with:\n{repr(failure)}')
        fail = 'unknown'
        if failure.check(HttpError):
            fail = 'HttpError'
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
        elif failure.check(DNSLookupError):
            fail = 'DNSLookupError'
            # this is the original request
        elif failure.check(TimeoutError):
            fail = 'TimeoutError'
        elif failure.check(TCPTimedOutError):
            fail = 'TCPTimedOutError'
        elif failure.check(ConnectionRefusedError):
            fail = 'ConnectionRefusedError'
        yield ProxyStatInc(proxy=proxy, success=0, seconds=0, fail=fail)

    def is_ok(self, response):
        return self.success_key in response.text

    def get_url(self, proxy=''):
        raise NotImplementedError


class HttpbinValidator(BaseValidator):
    name = 'vhttpbin'

    def __init__(self):
        super().__init__()
        self.origin_ip = requests.get('http://httpbin.org/ip').json().get(
            'origin')

    def get_url(self, proxy=''):
        if proxy.startswith('https'):
            return 'https://httpbin.org/ip'
        elif proxy.startswith('http'):
            return 'http://httpbin.org/ip'
        else:
            self.logger.warning(f'Unknown proxy: {proxy}')
            return 'http://httpbin.org'

    def is_ok(self, response):
        # example: 'http://198.211.121.46:80'
        try:
            ip = json.loads(response.text).get('origin')
        except Exception as e:
            self.logger.error(f'Unexpected error:{e}')
            return False
        if self.origin_ip in ip:
            self.logger.error(f'{proxy} is transparent')
            return False
        return True

