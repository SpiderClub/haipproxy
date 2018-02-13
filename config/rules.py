"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from config.settings import (
    SPIDER_COMMON_TASK, SPIDER_AJAX_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK,
    VALIDATED_HTTP_QUEUE, VALIDATED_HTTPS_QUEUE,
    VALIDATOR_HTTP_TASK, VALIDATOR_HTTPS_TASK,
    INIT_HTTP_QUEUE)


__all__ = ['CRWALER_TASKS', 'VALIDATOR_TASKS', 'CRAWLER_TASK_MAPS',
           'VALIDATOR_TASK_MAPS', 'RESOURCE_MAPS']


CRWALER_TASKS = [
    {
        'name': 'mogumiao',
        'resource': ['http://www.mogumiao.com/proxy/free/listFreeIp',
                     'http://www.mogumiao.com/proxy/api/freeIp?count=15'],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 5,
        'enable': 1,
    },
    {
        'name': 'xdaili',
        'resource': ['http://www.xdaili.cn:80/ipagent/freeip/getFreeIps?page=1&rows=10'],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 10,
        'enable': 1,
    },
    {
        'name': 'xici',
        'resource': ['http://www.xicidaili.com/nn/%s' % i for i in range(1, 6)] +
                    ['http://www.xicidaili.com/wn/%s' % i for i in range(1, 6)] +
                    ['http://www.xicidaili.com/wt/%s' % i for i in range(1, 6)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1
    },
    {
        'name': 'kuaidaili',
        'resource': ['https://www.kuaidaili.com/free/inha/%s' % i for i in range(1, 6)] +
                    ['https://www.kuaidaili.com/proxylist/%s' % i for i in range(1, 11)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1
    },
    {
        'name': 'kxdaili',
        'resource': [
            'http://www.kxdaili.com/dailiip/%s/%s.html#ip' % (i, j) for i in range(1, 3) for j in range(1, 11)
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1
    },
    {
        'name': 'mrhinkydink',
        'resource': ['http://www.mrhinkydink.com/proxies.htm'],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 2 * 60,
        'enable': 1,
    },
    {
        'name': 'nianshao',
        'resource': ['http://www.nianshao.me/?stype=1&page=%s' % i for i in range(1, 11)] +
                    ['http://www.nianshao.me/?stype=2&page=%s' % i for i in range(1, 11)] +
                    ['http://www.nianshao.me/?stype=5&page=%s' % i for i in range(1, 11)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1
    },
    {
        'name': '66ip',
        'resource': ['http://www.66ip.cn/%s.html' % i for i in range(1, 3)] +
                    ['http://www.66ip.cn/areaindex_%s/%s.html' % (i, j)
                     for i in range(1, 35) for j in range(1, 3)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 2 * 60,
        'enable': 1
    },
    {
        'name': 'baizhongsou',
        'resource': ['http://ip.baizhongsou.com/'],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 30,
        'enable': 1
    },
    {
        # there are some problems using crawlspider, so we use basic spider
        'name': 'coderbusy',
        'resource': ['https://proxy.coderbusy.com/'] +
                    ['https://proxy.coderbusy.com/classical/https-ready.aspx?page=%s' % i for i in range(1, 21)] +
                    ['https://proxy.coderbusy.com/classical/post-ready.aspx?page=%s' % i for i in range(1, 21)] +
                    ['https://proxy.coderbusy.com/classical/anonymous-type/anonymous.aspx?page=%s'
                     % i for i in range(1, 6)] +
                    ['https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page=%s'
                     % i for i in range(1, 6)] +
                    ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=%s' % i for i in range(1, 21)] +
                    ['https://proxy.coderbusy.com/classical/country/us.aspx?page=%s' % i for i in range(1, 11)] +
                    ['https://proxy.coderbusy.com/classical/country/id.aspx?page=%s' % i for i in range(1, 6)] +
                    ['https://proxy.coderbusy.com/classical/country/ru.aspx?page=%s' % i for i in range(1, 6)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 2 * 60,
        'enable': 1
    },
    {
        'name': 'data5u',
        'resource': [
            'http://www.data5u.com/free/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml'
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 10,
        'enable': 1,
    },
    {
        'name': 'httpsdaili',
        'resource': ['http://www.httpsdaili.com/?stype=1&page=%s' % i for i in range(1, 8)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'ip181',
        'resource': ['http://www.ip181.com/'] +
                    ['http://www.ip181.com/daili/%s.html' % i for i in range(1, 4)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 10,
        'enable': 1,
    },
    {
        'name': 'ip3366',
        'resource': ['http://www.ip3366.net/free/?stype=1&page=%s' % i for i in range(1, 3)] +
                    ['http://www.ip3366.net/free/?stype=3&page=%s' % i for i in range(1, 3)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 30,
        'enable': 1
    },
    {
        'name': 'iphai',
        'resource': [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wp',
            'http://www.iphai.com/'
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'swei360',
        'resource': ['http://www.swei360.com/free/?page=%s' % i for i in range(1, 4)] +
                    ['http://www.swei360.com/free/?stype=3&page=%s' % i for i in range(1, 4)],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 30,
        'enable': 1,
    },
    {
        'name': 'yundaili',
        'resource': [
            'http://www.yun-daili.com/free.asp?stype=1',
            'http://www.yun-daili.com/free.asp?stype=2',
            'http://www.yun-daili.com/free.asp?stype=3',
            'http://www.yun-daili.com/free.asp?stype=4',
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 6 * 60,
        'enable': 1,
    },
    {
        'name': 'ab57',
        'resource': [
            'http://ab57.ru/downloads/proxyold.txt',
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'proxylists',
        'resource': [
            'http://www.proxylists.net/http_highanon.txt',
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'my-proxy',
        'resource': [
            'https://www.my-proxy.com/free-elite-proxy.html',
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
            'https://www.my-proxy.com/free-socks-5-proxy.html'
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'us-proxy',
        'resource': [
            'https://www.us-proxy.org/',
            'https://free-proxy-list.net/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://free-proxy-list.net/anonymous-proxy.html',
            'https://www.socks-proxy.net/',
            'https://www.sslproxies.org/'
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'atomintersoft',
        'resource': [
            'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
            'http://www.atomintersoft.com/anonymous_proxy_list',
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'rmccurdy',
        'resource': [
            'https://www.rmccurdy.com/scripts/proxy/good.txt'
        ],
        'task_type': SPIDER_COMMON_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'proxydb',
        'resource': ['http://proxydb.net/?offset=%s' % (15 * i) for i in range(20)],
        'task_type': SPIDER_AJAX_TASK,
        'internal': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'cool-proxy',
        'resource': ['https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s'
                     % i for i in range(1, 11)],
        'task_type': SPIDER_AJAX_TASK,
        'internal': 30,
        'enable': 1,
    },
    {
        'name': 'goubanjia',
        'resource': ['http://www.goubanjia.com/'],
        'task_type': SPIDER_AJAX_TASK,
        'internal': 10,
        'enable': 1,
    },
    {
        'name': 'cn-proxy',
        'resource': [
            'http://cn-proxy.com/',
            'http://cn-proxy.com/archives/218'
        ],
        'task_type': SPIDER_GFW_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'xroxy',
        'resource': ['http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&'
                     'sort=reliability&desc=true&pnum=%s#table' % i for i in range(20)],
        'task_type': SPIDER_GFW_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'proxylistplus',
        'resource': [
            'http://list.proxylistplus.com/Socks-List-1',
            'http://list.proxylistplus.com/SSL-List-1'
        ],
        'task_type': SPIDER_GFW_TASK,
        'internal': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'cnproxy',
        'resource': ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)] +
                    ['http://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
        'task_type': SPIDER_AJAX_GFW_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'free-proxy',
        'resource': ['http://free-proxy.cz/en/proxylist/main/%s' % i for i in range(1, 30)],
        'task_type': SPIDER_AJAX_GFW_TASK,
        'internal': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'proxy-list',
        'resource': ['https://proxy-list.org/english/index.php?p=%s' % i for i in range(1, 11)],
        'task_type': SPIDER_AJAX_GFW_TASK,
        'internal': 60,
        'enable': 1,
    },
    {
        'name': 'gatherproxy',
        'resource': [
            'http://www.gatherproxy.com/',
            'http://www.gatherproxy.com/proxylist/anonymity/?t=Elite',
            'http://www.gatherproxy.com/proxylist/anonymity/?t=Anonymous',
            'http://www.gatherproxy.com/proxylist/country/?c=China',
            'http://www.gatherproxy.com/proxylist/country/?c=Brazil',
            'http://www.gatherproxy.com/proxylist/country/?c=Indonesia',
            'http://www.gatherproxy.com/proxylist/country/?c=Russia',
            'http://www.gatherproxy.com/proxylist/country/?c=United%20States',
            'http://www.gatherproxy.com/proxylist/country/?c=Thailand',
            'http://www.gatherproxy.com/proxylist/port/8080',
            'http://www.gatherproxy.com/proxylist/port/3128',
            'http://www.gatherproxy.com/proxylist/port/80',
            'http://www.gatherproxy.com/proxylist/port/8118'
        ],
        'task_type': SPIDER_AJAX_GFW_TASK,
        'internal': 60,
        'enable': 1,
    },
]


VALIDATOR_TASKS = [
    {
        'name': 'http',
        'task_type': VALIDATOR_HTTP_TASK,
        'resource': VALIDATED_HTTP_QUEUE,
        'internal': 2*60,  # 2 hours
        'enable': 1,
    },
    {
        'name': 'https',
        'task_type': VALIDATOR_HTTPS_TASK,
        'resource': VALIDATED_HTTPS_QUEUE,
        'internal': 2*60,  # 2 hours
        'enable': 1,
    },
]

# all the crawlers will fetch tasks from the following queues to execute
CRAWLER_TASK_MAPS = {
    'common': SPIDER_COMMON_TASK,
    'ajax': SPIDER_AJAX_TASK,
    'gfw': SPIDER_GFW_TASK,
    'ajax_gfw': SPIDER_AJAX_GFW_TASK
}

# all the validators will fetch proxies from the following queues to validate
VALIDATOR_TASK_MAPS = {
    'init': INIT_HTTP_QUEUE,
    'http': VALIDATOR_HTTP_TASK,
    'https': VALIDATOR_HTTPS_TASK
}

# all the clients will fetch resources from the following queues to use
RESOURCE_MAPS = {
    'http': VALIDATED_HTTP_QUEUE,
    'https': VALIDATED_HTTPS_QUEUE
}
