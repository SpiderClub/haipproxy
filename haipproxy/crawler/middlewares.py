"""
scrapy middlerwares for both downloader and spider
"""
import time

from ..config.settings import GFW_PROXY
from .user_agents import FakeChromeUA


class UserAgentMiddleware(object):
    """This middleware changes user agent randomly"""

    def process_request(self, request, spider):
        request.headers['User-Agent'] = FakeChromeUA.get_ua()
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'


class ProxyMiddleware(object):
    """This middleware provides http and https proxy for spiders"""

    def process_request(self, request, spider):
        # TODO: implement the code for spider.proxy_mode == 1, using proxy pools
        if not hasattr(spider, 'proxy_mode') or not spider.proxy_mode:
            return

        if spider.proxy_mode == 2:
            if 'splash' in request.meta:
                request.meta['splash']['args']['proxy'] = GFW_PROXY
            else:
                request.meta['proxy'] = GFW_PROXY


class RequestStartProfileMiddleware(object):
    """This middleware calculates the ip's speed"""

    def process_request(self, request, spider):
        request.meta['start'] = int(time.time() * 1000)


class RequestEndProfileMiddleware(object):
    """This middleware calculates the ip's speed"""

    def process_response(self, request, response, spider):
        speed = int(time.time() * 1000) - request.meta['start']
        request.meta['speed'] = speed
        return response
