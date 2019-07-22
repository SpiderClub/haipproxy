"""
scrapy middlerwares for both downloader and spider
"""
import re
import base64
import logging
import time

from fake_useragent import UserAgent
from sentry_sdk import capture_message

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import CloseSpider, IgnoreRequest
from scrapy.utils.misc import load_object
from scrapy.utils.response import response_status_message
from scrapy.utils.url import add_http_if_no_scheme

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


class RotatingProxyMiddleware(object):
    """
        DOWNLOADER_MIDDLEWARES = {
            # ...
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            # ...
        }
    It keeps track of dead and alive proxies and avoids using dead proxies.
    Proxy is considered dead if request.meta['_ban'] is True, and alive
    if request.meta['_ban'] is False; to set this meta key use
    BanDetectionMiddleware.

    By default, all default Scrapy concurrency options (DOWNLOAD_DELAY,
    AUTHTHROTTLE_..., CONCURRENT_REQUESTS_PER_DOMAIN, etc) become per-proxy
    for proxied requests when RotatingProxyMiddleware is enabled.
    For example, if you set CONCURRENT_REQUESTS_PER_DOMAIN=2 then
    spider will be making at most 2 concurrent connections to each proxy.

    Settings:
    * ``ROTATING_PROXY_PAGE_RETRY_TIMES`` - a number of times to retry
      downloading a page using a different proxy. After this amount of retries
      failure is considered a page failure, not a proxy failure.
      Think of it this way: every improperly detected ban cost you
      ``ROTATING_PROXY_PAGE_RETRY_TIMES`` alive proxies. Default: 10.
    """

    def __init__(self, max_proxies_to_try, crawler):
        self.pc = ProxyClient()
        self.max_proxies_to_try = max_proxies_to_try
        self.stats = crawler.stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            max_proxies_to_try=crawler.settings.getint(
                "ROTATING_PROXY_PAGE_RETRY_TIMES", 10
            ),
            crawler=crawler,
        )

    def process_request(self, request, spider):
        if "proxy" in request.meta and not request.meta.get("_rotating_proxy"):
            return
        protocol = "https" if request.url.startswith("https") else "http"
        proxy = next(self.pc.proxy_gen(protocol))
        if not proxy:
            raise CloseSpider("no_proxies")
        request.meta["proxy"] = proxy
        request.meta["download_slot"] = proxy
        request.meta["_rotating_proxy"] = True

    def process_exception(self, request, exception, spider):
        return self._handle_result(request, spider)

    def process_response(self, request, response, spider):
        return self._handle_result(request, spider) or response

    def _handle_result(self, request, spider):
        proxy = request.meta.get("proxy")
        if not (proxy and request.meta.get("_rotating_proxy")):
            return
        ban = request.meta.get("_ban", None)
        if ban:
            self.pc.mark_dead(proxy)
            return self._retry(request, spider)
        else:
            self.pc.mark_good(proxy)
        self.pc.set_stats(self.stats)

    def _retry(self, request, spider):
        retries = request.meta.get("proxy_retry_times", 0) + 1
        max_proxies_to_try = request.meta.get(
            "max_proxies_to_try", self.max_proxies_to_try
        )
        if retries <= max_proxies_to_try:
            logger.debug(
                "Retrying %(request)s with another proxy "
                "(failed %(retries)d times, "
                "max retries: %(max_proxies_to_try)d)",
                {
                    "request": request,
                    "retries": retries,
                    "max_proxies_to_try": max_proxies_to_try,
                },
                extra={"spider": spider},
            )
            retryreq = request.copy()
            retryreq.meta["proxy_retry_times"] = retries
            retryreq.dont_filter = True
            return retryreq
        else:
            logger.debug(
                "Gave up retrying %(request)s (failed %(retries)d "
                "times with different proxies)",
                {"request": request, "retries": retries},
                extra={"spider": spider},
            )


class BanDetectionPolicy(object):
    """ Default ban detection rules. """

    NOT_BAN_STATUSES = {200, 301, 302}
    NOT_BAN_EXCEPTIONS = (IgnoreRequest,)

    def response_is_ban(self, request, response):
        if response.status not in self.NOT_BAN_STATUSES:
            return True
        if response.status == 200 and not len(response.body):
            return True
        return False

    def exception_is_ban(self, request, exception):
        return not isinstance(exception, self.NOT_BAN_EXCEPTIONS)


class BanDetectionMiddleware(object):
    """
    Downloader middleware for detecting bans. It adds
    '_ban': True to request.meta if the response was a ban.

    To enable it, add it to DOWNLOADER_MIDDLEWARES option::
        DOWNLOADER_MIDDLEWARES = {
            # ...
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            # ...
        }

    By default, client is considered banned if a request failed, and alive
    if a response was received. You can override ban detection method by
    passing a path to a custom BanDectionPolicy in
    ``ROTATING_PROXY_BAN_POLICY``, e.g.::

    ROTATING_PROXY_BAN_POLICY = 'myproject.policy.MyBanPolicy'

    The policy must be a class with ``response_is_ban``
    and ``exception_is_ban`` methods. These methods can return True
    (ban detected), False (not a ban) or None (unknown). It can be convenient
    to subclass and modify default BanDetectionPolicy::

        # myproject/policy.py
        from rotating_proxies.policy import BanDetectionPolicy

        class MyPolicy(BanDetectionPolicy):
            def response_is_ban(self, request, response):
                # use default rules, but also consider HTTP 200 responses
                # a ban if there is 'captcha' word in response body.
                ban = super(MyPolicy, self).response_is_ban(request, response)
                ban = ban or b'captcha' in response.body
                return ban

            def exception_is_ban(self, request, exception):
                # override method completely: don't take exceptions in account
                return None

    Instead of creating a policy you can also implement ``response_is_ban``
    and ``exception_is_ban`` methods as spider methods, for example::

        class MySpider(scrapy.Spider):
            # ...

            def response_is_ban(self, request, response):
                return b'banned' in response.body

            def exception_is_ban(self, request, exception):
                return None

    """

    def __init__(self, stats, policy):
        self.stats = stats
        self.policy = policy

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats, cls._load_policy(crawler))

    @classmethod
    def _load_policy(cls, crawler):
        policy_path = crawler.settings.get(
            "ROTATING_PROXY_BAN_POLICY",
            "haipproxy.crawler.middlewares.BanDetectionPolicy",
        )
        policy_cls = load_object(policy_path)
        if hasattr(policy_cls, "from_crawler"):
            return policy_cls.from_crawler(crawler)
        else:
            return policy_cls()

    def process_response(self, request, response, spider):
        is_ban = getattr(spider, "response_is_ban", self.policy.response_is_ban)
        ban = is_ban(request, response)
        request.meta["_ban"] = ban
        if ban:
            self.stats.inc_value("bans/status/%s" % response.status)
            if not len(response.body):
                self.stats.inc_value("bans/empty")
        return response

    def process_exception(self, request, exception, spider):
        is_ban = getattr(spider, "exception_is_ban", self.policy.exception_is_ban)
        ban = is_ban(request, exception)
        if ban:
            ex_class = "%s.%s" % (
                exception.__class__.__module__,
                exception.__class__.__name__,
            )
            self.stats.inc_value("bans/error/%s" % ex_class)
        request.meta["_ban"] = ban
