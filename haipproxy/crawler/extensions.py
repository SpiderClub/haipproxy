from scrapy import signals
from sentry_sdk import capture_message


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
        try:
            failure.raiseException()
        except:
            message = 'error occurs when parsing {}'.format(response.url)
            capture_message(message)
        else:
            spider.logger.error("Error on {0}, traceback: {1}".format(
                response.url, failure.getTraceback()))
