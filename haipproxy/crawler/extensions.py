from scrapy import signals

from ..config.settings import USE_SENTRY
from ..utils.err_trace import client


# don't know why process_spider_exception in spidermiddleware
# can't be called, so we use extensions to workaround, for more
# information, see: https://github.com/scrapy/scrapy/issues/220
class FailLogger(object):
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()

        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        return ext

    def spider_error(self, failure, response, spider):
        if USE_SENTRY:
            try:
                failure.raiseException()
            except:
                message = 'error occurs when parsing {}'.format(response.url)
                client.captureException(message=message)
        else:
            spider.logger.error("Error on {0}, traceback: {1}".format(
                response.url, failure.getTraceback()))
