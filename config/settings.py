"""
Settings for global.
"""

# scrapy basic info
BOT_NAME = 'haiproxy'
SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# downloader settings
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 60
# to aviod infinite recursion
DEPTH_LIMIT = 3
# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'


# splush settings
SPLASH_URL = 'http://127.0.0.1:8050'


# extension settings
TELNETCONSOLE_ENABLED = False
EXTENSIONS = {
    'crawler.extensions.FailLogger': 500
}


DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.UserAgentMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# item pipeline settings
ITEM_PIPELINES = {
    'crawler.pipelines.ProxyIPPipeline': 200,
}

# scrapy log settings
LOG_LEVEL = 'DEBUG'


# custom spider settings
SPIDER_FEED_SIZE = 10
SPIDER_COMMON_TASK = 'haipproxy:common_task'
SPIDER_AJAX_TASK = 'haipproxy:ajax_task'
SPIDER_CRAWL_TASK = 'haipproxy:crawl_task'
SPIDER_GFW_TASK = 'haipproxy:gfw_task'

# redis args
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
DEFAULT_REDIS_DB = 0
META_DATA_DB = 1




