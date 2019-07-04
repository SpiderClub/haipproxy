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

from haipproxy.config.rules import (SPEED_QUEUE_MAPS, TTL_QUEUE_MAPS,
                                    SCORE_QUEUE_MAPS, HTTP_TASKS, HTTPS_TASKS)
from haipproxy.config.settings import (INIT_HTTP_Q, TEMP_HTTP_Q, TEMP_HTTPS_Q,
                                       VALIDATED_HTTP_Q, VALIDATED_HTTPS_Q,
                                       TTL_HTTP_Q, TTL_HTTPS_Q, SPEED_HTTP_Q,
                                       SPEED_HTTPS_Q)
from ..redis_spiders import RedisSpider, ValidatorRedisSpider
from ..items import ProxyScoreItem, ProxyVerifiedTimeItem, ProxySpeedItem, ProxyStatInc
from .base import BaseValidator


class HttpbinValidator(RedisSpider):
    name = 'vhttpbin'

    custom_settings = {
        'CONCURRENT_REQUESTS': 100,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 100,
        'RETRY_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'haipproxy.crawler.middlewares.RequestStartProfileMiddleware': 500,
            'haipproxy.crawler.middlewares.RequestEndProfileMiddleware': 500,
        },
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


class HttpValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of http proxy resources"""
    name = 'http'
    urls = [
        'http://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTP_Q
    score_queue = VALIDATED_HTTP_Q
    ttl_queue = TTL_HTTP_Q
    speed_queue = SPEED_HTTP_Q


class HttpsValidator(BaseValidator, ValidatorRedisSpider):
    """This validator checks the liveness of https proxy resources"""
    name = 'https'
    urls = [
        'https://httpbin.org/ip',
    ]
    task_queue = TEMP_HTTPS_Q
    score_queue = VALIDATED_HTTPS_Q
    ttl_queue = TTL_HTTPS_Q
    speed_queue = SPEED_HTTPS_Q
