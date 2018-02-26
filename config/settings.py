"""
Settings for global.
"""

# scrapy basic info
BOT_NAME = 'haiproxy'
SPIDER_MODULES = ['crawler.spiders', 'crawler.validators']
NEWSPIDER_MODULE = 'crawler'

# downloader settings
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 30
# to aviod infinite recursion
DEPTH_LIMIT = 100
CONCURRENT_REQUESTS = 50
# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
HTTPCACHE_ENABLED = False
GFW_PROXY = 'http://127.0.0.1:8123'

# splash settings
SPLASH_URL = 'http://127.0.0.1:8050'

# extension settings
RETRY_ENABLED = False
TELNETCONSOLE_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.UserAgentMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    # it should be before than HttpProxyMiddleware
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

# redis settings
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
DEFAULT_REDIS_DB = 0
META_DATA_DB = 0

# scheduler settings
TIMER_RECORDER = 'haipproxy:schduler:task'
LOCKER_PREFIX = 'haipproxy:lock:'

# custom spider settings
SPIDER_FEED_SIZE = 10
SPIDER_COMMON_TASK = 'haipproxy:spider:common'
SPIDER_AJAX_TASK = 'haipproxy:spider:ajax'
SPIDER_GFW_TASK = 'haipproxy:spider:gfw'
SPIDER_AJAX_GFW_TASK = 'haipproxy:spider:ajax_gfw'

# custom validator settings
VALIDATOR_FEED_SIZE = 50
# they are just temp tasks
# todo use set other than list
VALIDATOR_HTTP_TASK = 'haipproxy:validator:http'
VALIDATOR_HTTPS_TASK = 'haipproxy:validator:https'
VALIDATOR_WEIBO_TASK = 'haipproxy:validator:weibo'

# initially validator just classify ip resources into http and https queues, which can
# be stable or unstable

# stable and unstable validator will validate ip resources to ensure whenever the proxy
# is alive, so they do this job very frequently

# data_all is a set , it's a dupefilter
DATA_ALL = 'haipproxy:all'
# http_queue is a list, it's used to store initially http/https proxy resourecs
INIT_HTTP_QUEUE = 'haipproxy:init:http'
# socks proxy resources container
INIT_SOCKS4_QUEUE = 'haipproxy:init:socks4'
INIT_SOCKS5_QUEUE = 'haipproxy:init:socks5'

# valited queues are zsets.squid and other clients fetch ip resources from them.
VALIDATED_HTTP_QUEUE = 'haipproxy:http:validated'
VALIDATED_HTTPS_QUEUE = 'haipproxy:https:validated'

# it should be smaller than SQUID_UPDATE_INTERNAL
TTL_VALIDATED_TIME = 5  # minutes
TTL_HTTP_QUEUE = 'haipproxy:ttl:http'
TTL_HTTPS_QUEUE = 'haipproxy:ttl:https'

# squid settings
SQUID_BIN_PATH = '/usr/local/sbin/squid'  # mac os
SQUID_CONF_PATH = '/usr/local/etc/squid.conf'  # mac os
SQUID_TEMPLATE_PATH = '/usr/local/etc/squid.conf.backup'  # mac os
SQUID_UPDATE_INTERNAL = 10  # minutes
PROXY_BATCH_SIZE = 500
