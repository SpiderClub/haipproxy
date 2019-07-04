"""
Settings for global.
"""
#### Scrapy settings of this project ####
# scrapy basic info
BOT_NAME = 'googlebot'
# 注册的spider路径
SPIDER_MODULES = ['haipproxy.crawler.spiders', 'haipproxy.crawler.validators']

# downloader settings
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 30

# to aviod infinite recursion
DEPTH_LIMIT = 20
CONCURRENT_REQUESTS = 30

# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
HTTPCACHE_ENABLED = False
# 这是翻墙的URL，注意你如果用的是shadowsocks的话，需要将socks5其转为http协议，具体方法请阅读 https://rookiefly.cn/detail/201。请视具体情况修改 127.0.0.1
GFW_PROXY = 'http://127.0.0.1:8123'

# scrapy-splash URL，用于抓取ajax相关任务。
# splash settings.If you use docker-compose,SPLASH_URL = 'http://splash:8050'
SPLASH_URL = 'http://127.0.0.1:8050'

# extension settings
# RETRY_ENABLED = False
# TELNETCONSOLE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    'haipproxy.crawler.middlewares.UserAgentMiddleware': 543,
    'haipproxy.crawler.middlewares.ProxyMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    # it should be prior to HttpProxyMiddleware
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware':
    810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# scrapy log settings
LOG_LEVEL = 'INFO'

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
SPIDER_COMMON_Q = 'haipproxy:spider:common'
SPIDER_AJAX_Q = 'haipproxy:spider:ajax'
SPIDER_GFW_Q = 'haipproxy:spider:gfw'
SPIDER_AJAX_GFW_Q = 'haipproxy:spider:ajax_gfw'

# data_all is a set , it's a dupefilter
DATA_ALL = 'haipproxy:all'

# the data flow is init queue->validated_queue->validator_queue(temp)->validated_queue(score queue)->
# ttl_queue, speed_qeuue -> clients
# http_queue is a list, it's used to store initially http/https proxy resourecs
INIT_HTTP_Q = 'haipproxy:init:http'

# socks4/5代理存放的列表，目前项目并未对其进行校验和使用
# socks proxy resources container
INIT_SOCKS4_Q = 'haipproxy:init:socks4'
INIT_SOCKS5_Q = 'haipproxy:init:socks5'

# custom validator settings
VALIDATOR_FEED_SIZE = 50

# they are temp sets, come from init queue, in order to filter transparnt ip
TEMP_HTTP_Q = 'haipproxy:http:temp'
TEMP_HTTPS_Q = 'haipproxy:https:temp'
TEMP_WEIBO_Q = 'haipproxy:weibo:temp'
TEMP_ZHIHU_Q = 'haipproxy:zhihu:temp'

# 有序集合，用以存放验证过的IP及它们的分数
# valited queues are zsets.squid and other clients fetch ip resources from them.
VALIDATED_HTTP_Q = 'haipproxy:validated:http'
VALIDATED_HTTPS_Q = 'haipproxy:validated:https'
VALIDATED_WEIBO_Q = 'haipproxy:validated:weibo'
VALIDATED_ZHIHU_Q = 'haipproxy:validated:zhihu'

# 有序集合，用以存放验证过的IP及它们的最近验证时间
# time to live of proxy ip resources
TTL_VALIDATED_RESOURCE = 2  # minutes
TTL_HTTP_Q = 'haipproxy:ttl:http'
TTL_HTTPS_Q = 'haipproxy:ttl:https'
TTL_WEIBO_Q = 'haipproxy:ttl:weibo'
TTL_ZHIHU_Q = 'haipproxy:ttl:zhihu'

# 有序集合，用以存放验证过的IP及它们的响应速度，这里速度是最近一次响应速度，不是平均速度
# queue for proxy speed
SPEED_HTTP_Q = 'haipproxy:speed:http'
SPEED_HTTPS_Q = 'haipproxy:speed:https'
SPEED_WEIBO_Q = 'haipproxy:speed:weibo'
SPEED_ZHIHU_Q = 'haipproxy:speed:zhihu'

#### client settings ####
# 如果您需要使用squid作为二级代理，那么需要配置squid相关参数，以ubuntu为例
# squid settings on linux os
# execute sudo chown -R $USER /etc/squid/ and
# sudo chown -R $USER /var/log/squid/cache.log at first
SQUID_BIN_PATH = '/usr/sbin/squid'  # mac os '/usr/local/sbin/squid'
SQUID_CONF_PATH = '/etc/squid/squid.conf'  # mac os '/usr/local/etc/squid.conf'
# TEMPLATE file需要用户自己做拷贝
SQUID_TEMPLATE_PATH = '/etc/squid/squid.conf.backup'  # mac os /usr/local/etc/squid.conf.backup

# client picks proxies which's response time is between 0 and LONGEST_RESPONSE_TIME seconds
LONGEST_RESPONSE_TIME = 10

# client picks proxies which's score is not less than LOWEST_SCORE
LOWEST_SCORE = 6

# if the total num of proxies fetched is less than LOWES_TOTAL_PROXIES, haipproxy will fetch more
# more proxies with lower quality
LOWEST_TOTAL_PROXIES = 5

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
EXPORTER_LISTEN_HOST = '0.0.0.0'
EXPORTER_LISTEN_PORT = 7001
