"""
We use this validator to filter transparent ips, and give the ip resources an
initial score.
"""
import json
import requests

from json.decoder import JSONDecodeError
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (DNSLookupError, ConnectionRefusedError,
                                    TimeoutError, TCPTimedOutError)

from ..redis_spiders import RedisSpider
from ..items import ProxyStatInc


class HttpbinValidator(RedisSpider):
    name = 'vhttpbin'

    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'RETRY_ENABLED': False,
        'ITEM_PIPELINES': {
            'haipproxy.crawler.pipelines.ProxyStatPipeline': 200,
        }
    }
    success_key = ''

    def __init__(self):
        super().__init__()
        self.origin_ip = requests.get('http://httpbin.org/ip').json().get(
            'origin')

    def start_requests(self):
        for proxy in self.redis_conn.scan_iter(match='*://*'):
            proxy = proxy.decode()
            if proxy.startswith('https'):
                url = 'https://httpbin.org/ip'
            elif proxy.startswith('http'):
                url = 'http://httpbin.org/ip'
            else:
                self.logger.warning(f'Unknown proxy: {proxy}')
                continue
            req = Request(url,
                          meta={'proxy': proxy},
                          callback=self.parse,
                          errback=self.parse_error)
            yield req

    def parse(self, response):
        proxy = response.meta.get('proxy')
        seconds = int(response.meta.get('download_latency'))
        success = 1
        fail = ''
        if self.is_transparent(response):
            success = 0
            fail = 'transparent'
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

    def is_transparent(self, response):
        """filter transparent ip resources"""
        if not response.body_as_unicode():
            self.logger.error('no body')
            return True
        try:
            ip = json.loads(response.body_as_unicode()).get('origin')
            if self.origin_ip in ip:
                self.logger.error('is transparent ip')
                return True
        except (AttributeError, JSONDecodeError):
            self.logger.error('transparent ip AttributeError, JSONDecodeError')
            return True
        return False
