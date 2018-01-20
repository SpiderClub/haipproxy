"""
scrapy middlerwares for both downloader and spider
"""
from urllib.parse import urlsplit

from .user_agents import FakeChromeUA


class UserAgentMiddleware(object):
    """This middleware changes user agent by random"""
    def process_request(self, request, spider):
        request.headers['User-Agent'] = FakeChromeUA.get_ua()
        request.headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'


class ProxyMiddleware(object):
    """This middleware provides http and https proxy for spiders"""
    def process_request(self, request, spider):
        # todo 完善所有情况，如翻墙和普通代理
        if not spider.proxy_mode:
            return

        r = urlsplit(request.url)
        if spider.proxy_mode == 2:
            if r.scheme == 'https':
                request.meta['proxy'] = 'https://202.115.44.136:8123'
            else:
                request.meta['proxy'] = 'http://202.115.44.136:8123'

        # todo implement the code for spider.proxy_mode == 1, using proxy pools

