"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from haipproxy.config.settings import SPIDER_AJAX_Q, SPIDER_GFW_Q, SPIDER_AJAX_GFW_Q
# 代理抓取爬虫任务规则
# 本项目默认只抓匿名和高匿页面
# 爬虫任务类型，一共有四种类型，分别是:
# common(不需要翻墙，不需要ajax渲染),ajax(需要ajax渲染)
# gfw(需要翻墙)和ajax_gfw(需要翻墙和ajax渲染)
CRAWLER_TASKS = [
    {
        # > 3000 pages
        'name': 'xicidaili.com',
        'resource':
        ['http://www.xicidaili.com/nn/%s' % i for i in range(1, 6)] +
        ['http://www.xicidaili.com/wn/%s' % i for i in range(1, 6)] +
        ['http://www.xicidaili.com/wt/%s' % i for i in range(1, 6)],
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
            'split_detail': False,
            'protocols': None
        },
        # 定时抓取间隔，根据网站更新代理IP的时间间隔来定，单位是分钟
        'interval': 60,
        # 该规则是否生效
        'enable': 1
    },
    {
        'name': 'kuaidaili.com',
        'resource':
        ['https://www.kuaidaili.com/free/inha/%s' % i for i in range(1, 6)] +
        ['https://www.kuaidaili.com/proxylist/%s' % i for i in range(1, 11)],
        'parse_type': 'common',
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
        'interval': 60,
        'enable': 1
    },
    {
        'name': 'kxdaili.com',
        'resource':
        [f'http://ip.kxdaili.com/dailiip/1/{i}.html#ip' for i in range(1, 7)] + \
        [f'http://ip.kxdaili.com/dailiip/2/{i}.html#ip' for i in range(1, 5)],
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
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1
    },
    {
        'name': 'mrhinkydink.com',
        'resource': ['http://www.mrhinkydink.com/proxies.htm'],
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
        'name': 'ip181.com',
        'resource': ['http://www.ip181.com/'] +
        ['http://www.ip181.com/daili/%s.html' % i for i in range(1, 20)],
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
            'split_detail': False,
            'protocols': None
        },
        'interval': 10,
        'enable': 1,
    },
    {
        'name': 'ip3366.net',
        'resource': [
            'http://www.ip3366.net/free/?stype=1&page=%s' % i
            for i in range(1, 3)
        ] + [
            'http://www.ip3366.net/free/?stype=3&page=%s' % i
            for i in range(1, 3)
        ],
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
            'split_detail': False,
            'protocols': None
        },
        'interval': 30,
        'enable': 1
    },
    {
        'name': 'iphai.com',
        'resource': [
            'http://www.iphai.com/free/ng', 'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/np', 'http://www.iphai.com/free/wp',
            'http://www.iphai.com/'
        ],
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
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'ab57.ru',
        'resource': ['http://ab57.ru/downloads/proxyold.txt'],
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
        'name': 'my-proxy.com',
        'resource': [
            'https://www.my-proxy.com/free-elite-proxy.html',
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
            'https://www.my-proxy.com/free-socks-5-proxy.html'
        ],
        # if the parse method is specified, set it in the Spider's parser_maps
        'parse_type': 'myproxy',
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'us-proxy.org',
        'resource': ['https://www.us-proxy.org/'],
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
        'name': 'atomintersoft.com',
        'resource': [
            'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
            'http://www.atomintersoft.com/anonymous_proxy_list',
        ],
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
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'rmccurdy.com',
        'resource': ['https://www.rmccurdy.com/scripts/proxy/good.txt'],
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
        'name': 'coderbusy.com',
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
        'parse_type': 'common',
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
        'interval': 2 * 60,
        'enable': 1,
    },
    {
        'name': 'proxydb.net',
        'resource':
        ['http://proxydb.net/?offset=%s' % (15 * i) for i in range(20)],
        'parse_type': 'common',
        'parse_rule': {
            'detail_rule': 'a::text',
            'split_detail': True,
        },
        'interval': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'cool-proxy.net',
        'resource': [
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s'
            % i for i in range(1, 11)
        ],
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
        'interval': 30,
        'enable': 1,
    },
    {
        'name': 'goubanjia.com',
        'resource': ['http://www.goubanjia.com/'],
        'parse_type': 'goubanjia',
        'interval': 10,
        'enable': 1,
    },
    {
        'name': 'cn-proxy.com',
        'resource':
        ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218'],
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
        'name': 'free-proxy-list.net',
        'resource': [
            'https://free-proxy-list.net/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://free-proxy-list.net/anonymous-proxy.html',
        ],
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
        'name': 'xroxy',
        'resource': [
            'http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&'
            'sort=reliability&desc=true&pnum=%s#table' % i for i in range(20)
        ],
        'parse_type': 'xroxy',
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'proxylistplus',
        'resource': [
            'http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1',
            'http://list.proxylistplus.com/SSL-List-1'
        ],
        'parse_type': 'common',
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
        'interval': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'cnproxy.com',
        'resource':
        ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)] +
        ['http://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
        'parse_type': 'cnproxy',
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'free-proxy.cz',
        'resource': [
            'http://free-proxy.cz/en/proxylist/main/%s' % i
            for i in range(1, 30)
        ],
        'parse_type': 'free-proxy',
        'interval': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'proxy-list.org',
        'resource': [
            'https://proxy-list.org/english/index.php?p=%s' % i
            for i in range(1, 11)
        ],
        'parse_type': 'common',
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
        'interval': 60,
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
            'split_detail': False,
            'protocols': None
        },
        'interval': 60,
        'enable': 1,
    },
]

# crawler will fetch tasks from the following queues
CRAWLER_QUEUE_MAPS = {
    'ajax': SPIDER_AJAX_Q,
    'gfw': SPIDER_GFW_Q,
    'ajax_gfw': SPIDER_AJAX_GFW_Q
}

PARSE_MAP = {
    'xicidaili': {
        'row_xpath': '//table/tr[@class]',
        'ip_pos': 1,
        'port_pos': 2,
        'protocal_pos': 5
    },
    'kuaidaili': {
        'protocal_pos': 3
    }
}
