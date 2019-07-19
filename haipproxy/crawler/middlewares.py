"""
scrapy middlerwares for both downloader and spider
"""
import re
import base64
import logging
import time

from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from sentry_sdk import capture_message

from haipproxy.client import ProxyClient
from haipproxy.exceptions import HttpError, DownloadException

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault("User-Agent", self.ua.random)


class ErrorTraceMiddleware(object):
    def process_response(self, request, response, spider):
        if response.status >= 400:
            reason = "error http code {} for {}".format(response.status, request.url)
            self._faillog(request, HttpError, reason, spider)
        return response

    def process_exception(self, request, exception, spider):
        self._faillog(request, DownloadException, exception, spider)
        return

    def _faillog(self, request, exc, reason, spider):
        try:
            raise exc
        except Exception:
            message = "error occurs when downloading {}".format(request.url)
            capture_message(message)
        else:
            logger.error(reason)
