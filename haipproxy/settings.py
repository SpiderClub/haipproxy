# -*- coding: utf-8 -*-

# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "googlebot"

SPIDER_MODULES = ["haipproxy.crawler.spiders"]
# Module where to create new spiders using the genspider command.
NEWSPIDER_MODULE = "haipproxy.crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'tutorial (+http://www.yourdomain.com)'

# Obey robots.txt rules
# Cannot download proxies if follow robots.txt
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# This timeout can be set per spider using download_timeout
DOWNLOAD_TIMEOUT = 60

# Whether the Retry middleware will be enabled.
# RETRY_ENABLED = False

# Retry many times since proxies often fail
# RETRY_TIMES = 10

# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = "scrapy.dupefilters.BaseDupeFilter"

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": None,
    "haipproxy.crawler.middlewares.RandomUserAgentMiddleware": 400,
    "haipproxy.crawler.middlewares.RotatingProxyMiddleware": 610,
    "haipproxy.crawler.middlewares.BanDetectionMiddleware": 620,
}
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
#     'scrapy_proxies.RandomProxy': 100,
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'tutorial.pipelines.TutorialPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

LOG_LEVEL = "INFO"

MIN_PROXY_LEN = 9

# client picks proxies which's score is bigger than LOWEST_SCORE
LOWEST_SCORE = 0

#### Redis settings ####
# If you use docker-compose, REDIS_HOST = 'redis'
# if some value is empty, set like this: key = ''
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PIPE_BATCH_SIZE = 200

# scheduler settings
# 定时任务调度器设置，表示其在Redis中的Key
# 数据结构是一个hash表,存储了各个任务上次执行的时间
TIMER_RECORDER = "haipproxy:scheduler:task"
LOCKER_PREFIX = "haipproxy:lock:"

# proxies crawler's settings
# 每次从任务中获取的任务数，haipproxy并不保证消息不丢失
SPIDER_FEED_SIZE = 10
# 四个代理抓取的任务，分别为 common ajax gfw 和 ajax_gfw，下面是它们在Redis中的队列名，
SPIDER_AJAX_Q = "haipproxy:spider:ajax"
SPIDER_GFW_Q = "haipproxy:spider:gfw"
SPIDER_AJAX_GFW_Q = "haipproxy:spider:ajax_gfw"

#  这是翻墙的URL，注意你如果用的是shadowsocks的话，需要将socks5其转为http协议，具体方法请阅读 https://rookiefly.cn/detail/201。请视具体情况修改 127.0.0.1
GFW_PROXY = "http://127.0.0.1:8123"

#### client settings ####
# 如果您需要使用squid作为二级代理，那么需要配置squid相关参数，以ubuntu为例
# squid settings on linux os
# execute sudo chown -R $USER /etc/squid/ and
# sudo chown -R $USER /var/log/squid/cache.log at first
SQUID_BIN_PATH = "/usr/sbin/squid"  # mac os '/usr/local/sbin/squid'
SQUID_CONF_PATH = "/etc/squid/squid.conf"  # mac os '/usr/local/etc/squid.conf'
# TEMPLATE file需要用户自己做拷贝
SQUID_TEMPLATE_PATH = (
    "/etc/squid/squid.conf.backup"
)  # mac os /usr/local/etc/squid.conf.backup

# sentry for error tracking, for more information see
# https://github.com/getsentry/sentry
import sentry_sdk

sentry_sdk.init(
    # replace with your own path here.
    # use empty path to disable it
    "",
    debug=False,
)

# scrapy-splash URL，用于抓取ajax相关任务。
# splash settings.If you use docker-compose,SPLASH_URL = 'http://splash:8050'
SPLASH_URL = "http://127.0.0.1:8050"

# prometheus for monitoring, for more information see
# https://github.com/prometheus/prometheus
# you have to config prometheus first if you want to monitor haipproxy status
EXPORTER_LISTEN_HOST = "127.0.0.1"
EXPORTER_LISTEN_PORT = 7001
