"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from config.settings import (
    SPIDER_AJAX_TASK, SPIDER_CRAWL_TASK)

# todo: consider incremental crawling and incremental parser
# todo: consider filter transport ip
# todo: consider use socks5 to crawl the website outsite the wall
# todo: conbined the url of the same domain/according to spider type
URLS = [
    {
        'name': 'xici',
        'url_format': [
            'http://www.xicidaili.com/nn/{}'
        ],
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'kuaidaili',
        'url_format': [
            'https://www.kuaidaili.com/free/inha/{}'
        ],
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'kxdaili',
        'url_format': [
            'http://www.kxdaili.com/dailiip/1/{}.html#ip'
        ],
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'nianshao',
        'url_format': [
            'http://www.nianshao.me/?stype=1&page={}',
            'http://www.nianshao.me/?stype=2&page={}',
            'http://www.nianshao.me/?stype=5&page={}',
        ],
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'xdaili',
        'url_format': [
            'http://www.xdaili.cn:80/ipagent/freeip/getFreeIps?page=1&rows=10'
        ],
        'enable': 0,
    },
    {
        'name': 'goubanjia',
        'url_format': [
            'http://www.goubanjia.com/free/gngn/index{}.shtml',
            'http://www.goubanjia.com/free/gwgn/index{}.shtml'
        ],
        'start': 1,
        'end': 2,
        'enable': 0,
        'task_type': SPIDER_AJAX_TASK
    },
    {
        'name': '66ip',
        'url_format': ['http://www.66ip.cn/{}.html'] + [
            'http://www.66ip.cn/areaindex_%s/{}.html' % i for i in range(1, 35)],
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'baizhongsou',
        'url_format': [
            'http://ip.baizhongsou.com/'
        ],
        'enable': 0
    },
    {
        'name': 'coderbusy',
        'url_format': [
            'https://proxy.coderbusy.com/',
        ],
        'enable': 0,
        'task_type': SPIDER_CRAWL_TASK
    },
    {
        'name': 'data5u',
        'url_format': [
            'http://www.data5u.com/free/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml'
        ],
        'enable': 0,
    },
    {
        'name': 'httpsdaili',
        'url_format': [
            'http://www.httpsdaili.com/?stype=1',
            'http://www.httpsdaili.com/?stype=3',
        ],
        'enable': 0,
    },
    {
        'name': 'ip181',
        'url_format': ['http://www.ip181.com/'] + ['http://www.ip181.com/daili/%s.html' % i for i in range(1, 5)],
        'enable': 0,
    },
    {
        'name': 'ip3366',
        'url_format': [
            'http://www.ip3366.net/free/?stype=1&page={}',
            'http://www.ip3366.net/free/?stype=3&page={}'
        ],
        'start': 1,
        'end': 3,
        'enable': 0
    },
    {
        'name': 'iphai',
        'url_format': [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wp',
        ],
        'enable': 0,
    },
    {
        'name': 'yundaili',
        'url_format': [
            'http://www.yun-daili.com/free.asp?stype=1',
            'http://www.yun-daili.com/free.asp?stype=3',
        ],
        'enable': 1,
    },
]

# todo find a better way to extract ip infos
PARSER_RULES = {
    'goubanjia': {
        'ip': '',
        'port': '',
        'protocol': '',
        'method': 'xpath'
    }
}
