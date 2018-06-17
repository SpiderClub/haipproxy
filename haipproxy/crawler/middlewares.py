"""
scrapy middlerwares for both downloader and spider
"""
import time

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from ..exceptions import (
    HttpError, DownloadException
)
from ..config.settings import (
    GFW_PROXY, USE_SENTRY)
from ..utils.err_trace import client
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

        if spider.proxy_mode == 1:
            pass

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


class ErrorTraceMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status >= 400:
            reason = 'error http code {} for {}'.format(response.status, request.url)
            self._faillog(request, HttpError, reason, spider)
        return response

    def process_exception(self, request, exception, spider):
        self._faillog(request, DownloadException, exception, spider)
        return

    def _faillog(self, request, exc, reason, spider):
        if USE_SENTRY:
            try:
                raise exc
            except Exception:
                message = 'error occurs when downloading {}'.format(request.url)
                client.captureException(message=message)
        else:
            print(reason)


class ProxyRetryMiddleware(RetryMiddleware):
    def delete_proxy(self, proxy):
        pass

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            print('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            print('连接异常, 进行重试...')

            return self._retry(request, exception, spider)