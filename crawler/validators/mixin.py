"""
Useful mixin class for all the validators.
"""


class BaseSpider:
    # slow down each spider
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.RequestStartProfileMiddleware': 500,
            'crawler.middlewares.RequestEndProfileMiddleware': 500,
        }
    }

    def parse(self, response):
        speed = response.meta.get('speed')
        proxy = response.meta.get('proxy')
        self.parse_detail(response)

    def parse_detail(self, response):
        pass

    def parse_error(self, failure):
        request = failure.request
        proxy = request.meta.get('proxy')
        print('this proxy timeout', proxy)





