"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from ..config.settings import (
    SPIDER_COMMON_Q, SPIDER_AJAX_Q, SPIDER_GFW_Q, SPIDER_AJAX_GFW_Q,
    INIT_HTTP_Q, VALIDATED_HTTP_Q, VALIDATED_HTTPS_Q, TEMP_HTTP_Q,
    TEMP_HTTPS_Q, TTL_HTTP_Q, TTL_HTTPS_Q, SPEED_HTTPS_Q, SPEED_HTTP_Q,
    TEMP_WEIBO_Q, VALIDATED_WEIBO_Q, TTL_WEIBO_Q, SPEED_WEIBO_Q, TEMP_ZHIHU_Q,
    VALIDATED_ZHIHU_Q, TTL_ZHIHU_Q, SPEED_ZHIHU_Q)

CRAWLER_TASKS = [
    {
        # > 3000 pages
        'name': 'xicidaili.com',
        'resource':
        ['http://www.xicidaili.com/nn/%s' % i for i in range(1, 6)] +
        ['http://www.xicidaili.com/wn/%s' % i for i in range(1, 6)] +
        ['http://www.xicidaili.com/wt/%s' % i for i in range(1, 6)],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1
    },
    {
        'name':
        'kuaidaili.com',
        'resource':
        ['https://www.kuaidaili.com/free/inha/%s' % i for i in range(1, 6)] + \
        ['https://www.kuaidaili.com/proxylist/%s' % i for i in range(1, 11)],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 4,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1
    },
    {
        'name':
        'kxdaili.com',
        'resource':
        [f'http://ip.kxdaili.com/dailiip/1/{i}.html#ip' for i in range(1, 7)] + \
        [f'http://ip.kxdaili.com/dailiip/2/{i}.html#ip' for i in range(1, 5)],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1
    },
    {
        'name': 'mrhinkydink.com',
        'resource': ['http://www.mrhinkydink.com/proxies.htm'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'css',
            'pre_extract': '.text',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 2 * 60,
        'enable': 1,
    },
    {
        'name': 'baizhongsou.com',
        'resource': ['http://ip.baizhongsou.com/'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': True,
            'protocols': None
        },
        'interval': 30,
        'enable': 1
    },
    {
        'name':
        'ip181.com',
        'resource': ['http://www.ip181.com/'] +
        ['http://www.ip181.com/daili/%s.html' % i for i in range(1, 20)],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        10,
        'enable':
        1,
    },
    {
        'name':
        'ip3366.net',
        'resource': [
            'http://www.ip3366.net/free/?stype=1&page=%s' % i
            for i in range(1, 3)
        ] + [
            'http://www.ip3366.net/free/?stype=3&page=%s' % i
            for i in range(1, 3)
        ],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        30,
        'enable':
        1
    },
    {
        'name':
        'iphai.com',
        'resource': [
            'http://www.iphai.com/free/ng', 'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/np', 'http://www.iphai.com/free/wp',
            'http://www.iphai.com/'
        ],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name': 'ab57.ru',
        'resource': ['http://ab57.ru/downloads/proxyold.txt'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'text',
        'parse_rule': {
            'pre_extract': None,
            'delimiter': '\r\n',
            'redundancy': None,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'proxylists.net',
        'resource': ['http://www.proxylists.net/http_highanon.txt'],
        'parse_type': 'text',
        'task_queue': SPIDER_COMMON_Q,
        'parse_rule': {
            'pre_extract': None,
            'delimiter': '\r\n',
            'redundancy': None,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name':
        'my-proxy.com',
        'resource': [
            'https://www.my-proxy.com/free-elite-proxy.html',
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
            'https://www.my-proxy.com/free-socks-5-proxy.html'
        ],
        'task_queue':
        SPIDER_COMMON_Q,
        # if the parse method is specified, set it in the Spider's parser_maps
        'parse_type':
        'myproxy',
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name': 'us-proxy.org',
        'resource': ['https://www.us-proxy.org/'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tbody//tr',
            'infos_pos': 0,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'socks-proxy.net',
        'resource': [
            'https://www.socks-proxy.net/',
        ],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tbody//tr',
            'infos_pos': 0,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'sslproxies.org/',
        'resource': ['https://www.sslproxies.org/'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tbody//tr',
            'infos_pos': 0,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name':
        'atomintersoft.com',
        'resource': [
            'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
            'http://www.atomintersoft.com/anonymous_proxy_list',
        ],
        'task_queue':
        SPIDER_COMMON_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': True,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name': 'rmccurdy.com',
        'resource': ['https://www.rmccurdy.com/scripts/proxy/good.txt'],
        'task_queue': SPIDER_COMMON_Q,
        'parse_type': 'text',
        'parse_rule': {
            'pre_extract': None,
            'delimiter': '\n',
            'redundancy': None,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        # there are some problems using crawlspider, so we use basic spider
        'name':
        'coderbusy.com',
        'resource': ['https://proxy.coderbusy.com/'] + [
            'https://proxy.coderbusy.com/classical/https-ready.aspx?page=%s' %
            i for i in range(1, 21)
        ] + [
            'https://proxy.coderbusy.com/classical/post-ready.aspx?page=%s' % i
            for i in range(1, 21)
        ] + [
            'https://proxy.coderbusy.com/classical/anonymous-type/anonymous.aspx?page=%s'
            % i for i in range(1, 6)
        ] + [
            'https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page=%s'
            % i for i in range(1, 6)
        ] + [
            'https://proxy.coderbusy.com/classical/country/cn.aspx?page=%s' % i
            for i in range(1, 21)
        ] + [
            'https://proxy.coderbusy.com/classical/country/us.aspx?page=%s' % i
            for i in range(1, 11)
        ] + [
            'https://proxy.coderbusy.com/classical/country/id.aspx?page=%s' % i
            for i in range(1, 6)
        ] + [
            'https://proxy.coderbusy.com/classical/country/ru.aspx?page=%s' % i
            for i in range(1, 6)
        ],
        'task_queue':
        SPIDER_AJAX_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 1,
            'port_pos': 2,
            'extract_protocol': False,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        2 * 60,
        'enable':
        1,
    },
    {
        'name': 'proxydb.net',
        'resource':
        ['http://proxydb.net/?offset=%s' % (15 * i) for i in range(20)],
        'task_queue': SPIDER_AJAX_Q,
        'parse_type': 'common',
        'parse_rule': {
            'detail_rule': 'a::text',
            'split_detail': True,
        },
        'interval': 3 * 60,
        'enable': 1,
    },
    {
        'name':
        'cool-proxy.net',
        'resource': [
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s'
            % i for i in range(1, 11)
        ],
        'task_queue':
        SPIDER_AJAX_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': -1,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        30,
        'enable':
        1,
    },
    {
        'name': 'goubanjia.com',
        'resource': ['http://www.goubanjia.com/'],
        'task_queue': SPIDER_AJAX_Q,
        'parse_type': 'goubanjia',
        'interval': 10,
        'enable': 1,
    },
    {
        'name': 'cn-proxy.com',
        'resource':
        ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218'],
        'task_queue': SPIDER_GFW_Q,
        'parse_type': 'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tbody//tr',
            'infos_pos': 0,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name':
        'free-proxy-list.net',
        'resource': [
            'https://free-proxy-list.net/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://free-proxy-list.net/anonymous-proxy.html',
        ],
        'task_queue':
        SPIDER_GFW_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tbody//tr',
            'infos_pos': 0,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name':
        'xroxy',
        'resource': [
            'http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&'
            'sort=reliability&desc=true&pnum=%s#table' % i for i in range(20)
        ],
        'task_queue':
        SPIDER_GFW_Q,
        'parse_type':
        'xroxy',
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name':
        'proxylistplus',
        'resource': [
            'http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1',
            'http://list.proxylistplus.com/SSL-List-1'
        ],
        'task_queue':
        SPIDER_GFW_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr[contains(@class, "cells")]',
            'infos_pos': 1,
            'infos_end': -1,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': False,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        3 * 60,
        'enable':
        1,
    },
    {
        'name':
        'cnproxy.com',
        'resource':
        ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)] +
        ['http://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
        'task_queue':
        SPIDER_AJAX_GFW_Q,
        'parse_type':
        'cnproxy',
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name':
        'free-proxy.cz',
        'resource': [
            'http://free-proxy.cz/en/proxylist/main/%s' % i
            for i in range(1, 30)
        ],
        'task_queue':
        SPIDER_AJAX_GFW_Q,
        'parse_type':
        'free-proxy',
        'interval':
        3 * 60,
        'enable':
        1,
    },
    {
        'name':
        'proxy-list.org',
        'resource': [
            'https://proxy-list.org/english/index.php?p=%s' % i
            for i in range(1, 11)
        ],
        'task_queue':
        SPIDER_AJAX_GFW_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'css',
            'pre_extract': '.table ul',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'li::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': True,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1,
    },
    {
        'name':
        'gatherproxy',
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
        'task_queue':
        SPIDER_AJAX_GFW_Q,
        'parse_type':
        'common',
        'parse_rule': {
            'pre_extract_method': 'xpath',
            'pre_extract': '//tr',
            'infos_pos': 1,
            'infos_end': None,
            'detail_rule': 'td::text',
            'ip_pos': 0,
            'port_pos': 1,
            'extract_protocol': True,
            'split_detail': False,
            'protocols': None
        },
        'interval':
        60,
        'enable':
        1,
    },
]

# crawler will fetch tasks from the following queues
CRAWLER_QUEUE_MAPS = {
    'common': SPIDER_COMMON_Q,
    'ajax': SPIDER_AJAX_Q,
    'gfw': SPIDER_GFW_Q,
    'ajax_gfw': SPIDER_AJAX_GFW_Q
}

# validator scheduler will fetch tasks from resource queue and store into task queue
VALIDATOR_TASKS = [
    {
        'name': 'http',
        'task_queue': TEMP_HTTP_Q,
        'resource': VALIDATED_HTTP_Q,
        'interval': 5,  # 20 minutes
        'enable': 1,
    },
    {
        'name': 'https',
        'task_queue': TEMP_HTTPS_Q,
        'resource': VALIDATED_HTTPS_Q,
        'interval': 5,
        'enable': 1,
    },
    {
        'name': 'weibo',
        'task_queue': TEMP_WEIBO_Q,
        'resource': VALIDATED_WEIBO_Q,
        'interval': 5,
        'enable': 1,
    },
    {
        'name': 'zhihu',
        'task_queue': TEMP_ZHIHU_Q,
        'resource': VALIDATED_ZHIHU_Q,
        'interval': 5,
        'enable': 1,
    },
]

# validators will fetch proxies from the following queues
TEMP_QUEUE_MAPS = {
    'init': INIT_HTTP_Q,
    'http': TEMP_HTTP_Q,
    'https': TEMP_HTTPS_Q,
    'weibo': TEMP_WEIBO_Q,
    'zhihu': TEMP_ZHIHU_Q
}

# target website that use http protocol
HTTP_TASKS = ['http']

# target website that use https protocol
HTTPS_TASKS = ['https', 'zhihu', 'weibo']

# todo the three maps may be combined in one map
# validator scheduler and clients will fetch proxies from the following queues
SCORE_QUEUE_MAPS = {
    'http': VALIDATED_HTTP_Q,
    'https': VALIDATED_HTTPS_Q,
    'weibo': VALIDATED_WEIBO_Q,
    'zhihu': VALIDATED_ZHIHU_Q
}

# validator scheduler and clients will fetch proxies from the following queues which are verified recently
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
