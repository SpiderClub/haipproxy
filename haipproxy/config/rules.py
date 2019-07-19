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
        # there are some problems using crawlspider, so we use basic spider
        'name': 'coderbusy.com', # SPIDER_AJAX_TASK
        'resource': ['https://proxy.coderbusy.com/'],
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
        'name': 'proxydb.net', # SPIDER_AJAX_TASK
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
        'name': 'cool-proxy.net', # SPIDER_AJAX_TASK
        'resource': [
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s'
            % i for i in range(1, 11)
        ],
        'parse_type': 'common',
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
        'name': 'goubanjia.com', # SPIDER_AJAX_TASK
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
        'name': 'cnproxy.com', # SPIDER_AJAX_GFW_TASK
        'resource':
        ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)] +
        ['http://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
        'parse_type': 'cnproxy',
        'interval': 60,
        'enable': 1,
    },
    {
        'name': 'free-proxy.cz', # SPIDER_AJAX_GFW_TASK
        'resource': [
            'http://free-proxy.cz/en/proxylist/main/%s' % i
            for i in range(1, 30)
        ],
        'parse_type': 'free-proxy',
        'interval': 3 * 60,
        'enable': 1,
    },
    {
        'name': 'proxy-list.org', # SPIDER_AJAX_GFW_TASK
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
        'name': 'gatherproxy', # SPIDER_AJAX_GFW_TASK
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

