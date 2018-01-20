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
DOWNLOAD_TIMEOUT = 30
# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# extension settings
TELNETCONSOLE_ENABLED = False
EXTENSIONS = {
   'crawler.extensions.FailLogger': 500
}


DOWNLOADER_MIDDLEWARES = {
   'crawler.middlewares.UserAgentMiddleware': 543,
   'crawler.middlewares.ProxyMiddleware': 543,
}


# item pipeline settings
ITEM_PIPELINES = {
   'crawler.pipelines.ProxyIPPipeline': 200,
}

# scrapy log settings
LOG_LEVEL = 'DEBUG'


# custom spider settings
SPIDER_FEED_SIZE = 10
SPIDER_TASK_QUEUE = 'haipproxy:ip_task'

# redis args
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
DEFAULT_REDIS_DB = 0
META_DATA_DB = 1




