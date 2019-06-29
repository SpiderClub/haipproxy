由于[haipproxy](https://github.com/SpiderClub/haipproxy)配置文件参数众多，所以
单独写一篇文档对其做介绍。

配置文件位于[config](https://github.com/SpiderClub/haipproxy/tree/master/config)
目录下，具体有[settings.py](https://github.com/SpiderClub/haipproxy/blob/master/config/settings.py)
和[rules.py](https://github.com/SpiderClub/haipproxy/blob/master/config/rules.py)。
前者是项目默认的一些配置，包括`scrapy`的配置和`haipproxy`的一些配置；后者的作用是**配置代理IP源抓取规则**和**代理IP存
储映射相关规则**。具体参数意义请阅读下文。

---

### settings.py

```python3
#####################################################################
# scrapy相关设置
#####################################################################
# scrapy基本信息
BOT_NAME = 'haiproxy'
# 注册的spider路径
SPIDER_MODULES = ['crawler.spiders', 'crawler.validators']
NEWSPIDER_MODULE = 'crawler'
# scrapy downloader 设置
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 30
# 最大抓取深度，以防无限递归
DEPTH_LIMIT = 100
CONCURRENT_REQUESTS = 50
# don't filter anything, also can set dont_filter=True in Request objects
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
HTTPCACHE_ENABLED = False
# 这是翻墙的URL，注意你如果用的是shadowsocks的话，需要将socks5其转为http协议，具体方法
# 请阅读 https://rookiefly.cn/detail/201。请视具体情况修改 127.0.0.1
GFW_PROXY = 'http://127.0.0.1:8123'

# scrapy-splash URL，用于抓取ajax相关任务。请视具体情况修改 127.0.0.1 ，如果是使用的
# docker compose启动，请修改为 http://splash:8050
SPLASH_URL = 'http://127.0.0.1:8050'

# 关闭scrapy 某些扩展，以提高抓取效率
RETRY_ENABLED = False
TELNETCONSOLE_ENABLED = False
# scrapy下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.UserAgentMiddleware': 543,
    'crawler.middlewares.ProxyMiddleware': 543,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    # it should be before than HttpProxyMiddleware
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
# spider中间件
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

#####################################################################
# HAipproxy的默认设置
#####################################################################
# redis设置。如果你使用docker compose，请将 '127.0.0.1' 改成 'redis'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
META_DATA_DB = 0

# 定时任务调度器设置，表示其在Redis中的Key
# 数据结构是一个hash表,存储了各个任务上次执行的时间
TIMER_RECORDER = 'haipproxy:schduler:task'
LOCKER_PREFIX = 'haipproxy:lock:' # Redis分布式锁的前缀

# 代理抓取爬虫设置
# 每次从任务中获取的任务数，由于haipproxy并不保证消息不丢失，所以用户需要根据自己情况做权衡
SPIDER_FEED_SIZE = 10
# 四个代理抓取的任务，分别为 common ajax gfw 和 ajax_gfw，下面是它们在Redis中的队列名，
SPIDER_COMMON_Q = 'haipproxy:spider:common'
SPIDER_AJAX_Q = 'haipproxy:spider:ajax'
SPIDER_GFW_Q = 'haipproxy:spider:gfw'
SPIDER_AJAX_GFW_Q = 'haipproxy:spider:ajax_gfw'

# 存储所有代理IP，数据结构是一个set，用作过滤器
DATA_ALL = 'haipproxy:all'
# 数据流 init queue->validated_queue->validator_queue(temp)->validated_queue(score queue)->
# ttl_queue, speed_qeuue -> clients
# http_queue是一个列表,用以存放刚抓取到的http/https代理
INIT_HTTP_Q = 'haipproxy:init:http'
# socks4/5代理存放的列表，目前项目并未对其进行校验和使用
INIT_SOCKS4_Q = 'haipproxy:init:socks4'
INIT_SOCKS5_Q = 'haipproxy:init:socks5'

# 校验器批量任务获取数据量
VALIDATOR_FEED_SIZE = 50
# 从init queue获取到的临时集合,目的是对透明代理做一次过滤
TEMP_HTTP_Q = 'haipproxy:http:temp'
TEMP_HTTPS_Q = 'haipproxy:https:temp'
TEMP_WEIBO_Q = 'haipproxy:weibo:temp'
TEMP_ZHIHU_Q = 'haipproxy:zhihu:temp'

# 有序集合，用以存放验证过的IP及它们的分数
VALIDATED_HTTP_Q = 'haipproxy:validated:http'
VALIDATED_HTTPS_Q = 'haipproxy:validated:https'
VALIDATED_WEIBO_Q = 'haipproxy:validated:weibo'
VALIDATED_ZHIHU_Q = 'haipproxy:validated:zhihu'

# 有序集合，用以存放验证过的IP及它们的最近验证时间
TTL_VALIDATED_RESOURCE = 2  # minutes
TTL_HTTP_Q = 'haipproxy:ttl:http'
TTL_HTTPS_Q = 'haipproxy:ttl:https'
TTL_WEIBO_Q = 'haipproxy:ttl:weibo'
TTL_ZHIHU_Q = 'haipproxy:ttl:zhihu'

# 有序集合，用以存放验证过的IP及它们的响应速度，这里速度是最近一次响应速度，不是平均速度
SPEED_HTTP_Q = 'haipproxy:speed:http'
SPEED_HTTPS_Q = 'haipproxy:speed:https'
SPEED_WEIBO_Q = 'haipproxy:speed:weibo'
SPEED_ZHIHU_Q = 'haipproxy:speed:zhihu'

# 如果您需要使用squid作为二级代理，那么需要配置squid相关参数，以ubuntu为例
# 首先执行 sudo chown -R $USER /etc/squid/
# 再执行 sudo chown -R $USER /var/log/squid/cache.log
SQUID_BIN_PATH = '/usr/sbin/squid'  # macs上，路径为'/usr/local/sbin/squid'
SQUID_CONF_PATH = '/etc/squid/squid.conf'  # mac上，路径为 '/usr/local/etc/squid.conf'
# TEMPLATE file需要用户自己做拷贝
SQUID_TEMPLATE_PATH = '/etc/squid/squid.conf.backup'  # mac上，路径为 /usr/local/etc/squid.conf.backup

# 客户端设置
# 客户端只会选择响应时间在10s内的代理IP
LONGEST_RESPONSE_TIME = 10
# 客户端只会选择最低分数为7分的代理IP
LOWEST_SCORE = 7
```


### rules.py

```python3
# 代理抓取爬虫任务规则
CRAWLER_TASKS = [
    {
        # 代理IP源名，不能重复，建议选取域名
        'name': 'mogumiao',
        # 需要抓取的代理IP链接，您可以根据实际情况进行指定，本项目默认只抓匿名和高匿页面
        'resource': ['http://www.mogumiao.com/proxy/free/listFreeIp',
                     'http://www.mogumiao.com/proxy/api/freeIp?count=15'],
        # 爬虫任务类型，一共有四种类型，分别是 common(不需要翻墙，不需要ajax渲染),ajax(需要ajax渲染)
        # gfw(需要翻墙)和ajax_gfw(需要翻墙和ajax渲染)
        'task_queue': SPIDER_COMMON_Q,
        # 定时抓取间隔，根据网站更新代理IP的时间间隔来定，单位是分钟
        'interval': 5,
        # 该规则是否生效
        'enable': 1,
    }
]

# 代理IP抓取爬虫对应映射
CRAWLER_QUEUE_MAPS = {
    'common': SPIDER_COMMON_Q,
    'ajax': SPIDER_AJAX_Q,
    'gfw': SPIDER_GFW_Q,
    'ajax_gfw': SPIDER_AJAX_GFW_Q
}


# 校验器将从task_queue中获取代理IP，校验后存入resource，具体流程见 架构篇
VALIDATOR_TASKS = [
    {
        # 任务名，不能和其他任务同名
        'name': 'http',
        # 代理来源
        'task_queue': TEMP_HTTP_Q,
        # 代理存入的地方
        'resource': VALIDATED_HTTP_Q,
        # 定时校验间隔
        'interval': 20,
        # 是否启用
        'enable': 1,
    },
    {
        'name': 'zhihu',
        'task_queue': TEMP_ZHIHU_Q,
        'resource': VALIDATED_ZHIHU_Q,
        'interval': 20,
        'enable': 1,
    },
]

# 校验器将从下面队列中获取代理IP进行校验
TEMP_QUEUE_MAPS = {
    # init队列必须设置
    'init': INIT_HTTP_Q,
    'http': TEMP_HTTP_Q,
    'zhihu': TEMP_ZHIHU_Q
}

# 以下三个maps的作用是存储和提供可用代理，代表三个维度
SCORE_QUEUE_MAPS = {
    'http': VALIDATED_HTTP_Q,
    'https': VALIDATED_HTTPS_Q,
    'weibo': VALIDATED_WEIBO_Q,
    'zhihu': VALIDATED_ZHIHU_Q
}

TTL_QUEUE_MAPS = {
    'http': TTL_HTTP_Q,
    'https': TTL_HTTPS_Q,
    'weibo': TTL_WEIBO_Q,
    'zhihu': TTL_ZHIHU_Q
}

SPEED_QUEUE_MAPS = {
    'http': SPEED_HTTP_Q,
    'https': SPEED_HTTPS_Q,
    'weibo': SPEED_WEIBO_Q,
    'zhihu': SPEED_ZHIHU_Q
}
```
