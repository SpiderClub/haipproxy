import json
import pdb
import requests
import sys

from json.decoder import JSONDecodeError
from scrapy.http import Request
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import (
    DNSLookupError,
    ConnectionRefusedError,
    TimeoutError,
    TCPTimedOutError,
    ConnectError,
)

from .redis_spiders import RedisSpider
from haipproxy.crawler.items import ProxyStatInc


class BaseValidator(RedisSpider):
    # per test, both http and https proxies respond https request equally,
    # while https proxies don't response http request
    # It's common that a proxy succeed on other sites but not on httpbin
    custom_settings = {
        "CONCURRENT_REQUESTS": 100,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 100,
        "RETRY_ENABLED": False,
        "RETRY_TIMES": 0,
        "ITEM_PIPELINES": {"haipproxy.crawler.pipelines.ProxyStatPipeline": 200},
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
            "haipproxy.crawler.middlewares.RandomUserAgentMiddleware": 400,
        },
    }
    success_key = ""
    good_count = 0

    def start_requests(self):
        for proxy in self.redis_conn.scan_iter(match="*://*"):
            if self.redis_conn.hget(proxy, "used_count") > b"1":
                continue
            proxy = proxy.decode()
            req = Request(
                self.get_url(proxy),
                dont_filter=True,
                meta={"proxy": proxy},
                callback=self.parse,
                errback=self.parse_error,
            )
            yield req

    def parse(self, response):
        proxy = response.meta.get("proxy")
        seconds = int(response.meta.get("download_latency"))
        success = 1
        fail = ""
        if not self.is_ok(response):
            success = 0
            fail = "badcontent"
            self.logger.error(f"{proxy} got bad content")
        else:
            self.good_count += 1
            self.logger.info(f"good ip {self.good_count} {proxy}  ####")
        yield ProxyStatInc(proxy=proxy, success=success, seconds=seconds, fail=fail)

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get("proxy")
        self.logger.warning(f"proxy {proxy} has failed with:\n{repr(failure)}")
        fail = "unknown"
        if failure.check(HttpError):
            fail = "HttpError"
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
        elif failure.check(DNSLookupError):
            fail = "DNSLookupError"
            # this is the original request
        elif failure.check(TimeoutError):
            fail = "TimeoutError"
        elif failure.check(TCPTimedOutError):
            fail = "TCPTimedOutError"
        elif failure.check(ConnectionRefusedError):
            fail = "ConnectionRefusedError"
        elif failure.check(ConnectError):
            # port exhaustion: no more ports for connection
            # netsh int ipv4 set dynamicport tcp start=10000 num=55535
            pdb.set_trace()
            fail = "ConnectError"
        yield ProxyStatInc(proxy=proxy, success=0, seconds=0, fail=fail)

    def is_ok(self, response):
        # TODO: check len(response.text)
        return self.success_key in response.text

    def get_url(self, proxy=""):
        raise NotImplementedError


class HttpbinValidator(BaseValidator):
    name = "vhttpbin"

    def __init__(self):
        super().__init__()
        self.origin_ip = requests.get("http://httpbin.org/ip").json().get("origin")

    def get_url(self, proxy=""):
        if proxy.startswith("https"):
            return "https://httpbin.org/ip"
        elif proxy.startswith("http"):
            return "http://httpbin.org/ip"
        else:
            self.logger.warning(f"Unknown proxy: {proxy}")
            return "http://httpbin.org"

    def is_ok(self, response):
        # example: 'http://198.211.121.46:80'
        try:
            ip = json.loads(response.text).get("origin")
        except Exception as e:
            self.logger.error(f"Unexpected error:{e}")
            return False
        if self.origin_ip in ip:
            self.logger.error(f"{proxy} is transparent")
            return False
        return True


class CctvValidator(BaseValidator):
    name = "vcctv"

    def __init__(self):
        self.success_key = "中央电视台"

    def get_url(self, proxy=""):
        return "http://www.cctv.com/"


class UqerValidator(BaseValidator):
    name = "vuqer"

    def __init__(self):
        self.success_key = "优矿"

    def get_url(self, proxy=""):
        return "https://uqer.io/"
