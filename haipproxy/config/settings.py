"""
Settings for global.
"""
#### Scrapy settings of this project ####
# scrapy basic info
BOT_NAME = 'googlebot'
# 注册的spider路径
SPIDER_MODULES = ['haipproxy.crawler.spiders']

# downloader settings
# Cannot download if follow robots.txt
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 60

# to aviod infinite recursion
DEPTH_LIMIT = 20
CONCURRENT_REQUESTS = 30

# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
# 这是翻墙的URL，注意你如果用的是shadowsocks的话，需要将socks5其转为http协议，具体方法请阅读 https://rookiefly.cn/detail/201。请视具体情况修改 127.0.0.1
GFW_PROXY = 'http://127.0.0.1:8123'

# scrapy-splash URL，用于抓取ajax相关任务。
# splash settings.If you use docker-compose,SPLASH_URL = 'http://splash:8050'
SPLASH_URL = 'http://127.0.0.1:8050'

# extension settings
# RETRY_ENABLED = False
# TELNETCONSOLE_ENABLED = False
DOWNLOADER_MIDDLEWARES = {
    'haipproxy.crawler.middlewares.ProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'haipproxy.crawler.middlewares.RandomUserAgentMiddleware': 400,
}

# scrapy log settings
LOG_LEVEL = 'INFO'

MIN_PROXY_LEN = 9
#### Redis settings ####
# If you use docker-compose, REDIS_HOST = 'redis'
# if some value is empty, set like this: key = ''
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PIPE_BATCH_SIZE = 200

# scheduler settings
# 定时任务调度器设置，表示其在Redis中的Key
# 数据结构是一个hash表,存储了各个任务上次执行的时间
TIMER_RECORDER = 'haipproxy:scheduler:task'
LOCKER_PREFIX = 'haipproxy:lock:'

# proxies crawler's settings
# 每次从任务中获取的任务数，haipproxy并不保证消息不丢失
SPIDER_FEED_SIZE = 10
# 四个代理抓取的任务，分别为 common ajax gfw 和 ajax_gfw，下面是它们在Redis中的队列名，
SPIDER_AJAX_Q = 'haipproxy:spider:ajax'
SPIDER_GFW_Q = 'haipproxy:spider:gfw'
SPIDER_AJAX_GFW_Q = 'haipproxy:spider:ajax_gfw'

#### client settings ####
# 如果您需要使用squid作为二级代理，那么需要配置squid相关参数，以ubuntu为例
# squid settings on linux os
# execute sudo chown -R $USER /etc/squid/ and
# sudo chown -R $USER /var/log/squid/cache.log at first
SQUID_BIN_PATH = '/usr/sbin/squid'  # mac os '/usr/local/sbin/squid'
SQUID_CONF_PATH = '/etc/squid/squid.conf'  # mac os '/usr/local/etc/squid.conf'
# TEMPLATE file需要用户自己做拷贝
SQUID_TEMPLATE_PATH = '/etc/squid/squid.conf.backup'  # mac os /usr/local/etc/squid.conf.backup

# client picks proxies which's score is bigger than LOWEST_SCORE
LOWEST_SCORE = 0

#### monitor and bug trace ####
# sentry for error tracking, for more information see
# https://github.com/getsentry/sentry
import sentry_sdk
sentry_sdk.init(
    # replace with your own path here.
    # use empty path to disable it
    '',
    debug=False,
)

# prometheus for monitoring, for more information see
# https://github.com/prometheus/prometheus
# you have to config prometheus first if you want to monitor haipproxy status
EXPORTER_LISTEN_HOST = '127.0.0.1'
EXPORTER_LISTEN_PORT = 7001
