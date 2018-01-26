"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from config.settings import (
    SPIDER_AJAX_TASK, SPIDER_CRAWL_TASK,
    SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK)

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
            'https://www.kuaidaili.com/free/inha/{}',
            'https://www.kuaidaili.com/proxylist/{}'
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
        'task_type': SPIDER_AJAX_TASK,
        'enable': 0,
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
        'task_type': SPIDER_CRAWL_TASK,
        'enable': 0,
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
            'http://www.httpsdaili.com/?stype=1&page={}',
            'http://www.httpsdaili.com/?stype=2&page={}',
            'http://www.httpsdaili.com/?stype=3&page={}',
            'http://www.httpsdaili.com/?stype=4&page={}',
        ],
        'start': 1,
        'end': 3, # max 7
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
            'http://www.iphai.com/'
        ],
        'enable': 0,
    },
    {
        'name': 'swei360',
        'url_format': [
            'http://www.swei360.com/free/?page={}',
            'http://www.swei360.com/free/?stype=3&page={}',
        ],
        'start': 1,
        'end': 2, # max 7
        'enable': 1,
    },
    {
        'name': 'yundaili',
        'url_format': [
            'http://www.yun-daili.com/free.asp?stype=1',
            'http://www.yun-daili.com/free.asp?stype=3',
        ],
        'enable': 0,
    },
    {
        'name': 'cn-proxy',
        'url_format': [
            'http://cn-proxy.com/',
            'http://cn-proxy.com/archives/218'
        ],
        'task_type': SPIDER_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'proxydb',
        'url_format': [
            'http://proxydb.net/?offset={}',
        ],
        'start': 0,
        'offset': 15,
        'end': 0,
        'task_type': SPIDER_AJAX_TASK,
        'enable': 0,
    },
    {
        'name': 'ab57',
        'url_format': [
            'http://ab57.ru/downloads/proxyold.txt',
        ],
        'enable': 0,
    },
    {
        'name': 'proxylists',
        'url_format': [
            'http://www.proxylists.net/http_highanon.txt',
        ],
        'enable': 0,
    },
    {
        'name': 'my-proxy',
        'url_format': [
            'https://www.my-proxy.com/free-elite-proxy.html',
            'https://www.my-proxy.com/free-anonymous-proxy.html',
            'https://www.my-proxy.com/free-socks-4-proxy.html',
            'https://www.my-proxy.com/free-socks-5-proxy.html'
        ],
        'enable': 0,
    },
    {
        'name': 'us-proxy',
        'url_format': [
            'https://www.us-proxy.org/',
            'https://free-proxy-list.net/',
            'https://free-proxy-list.net/uk-proxy.html',
            'https://free-proxy-list.net/anonymous-proxy.html',
            'https://www.socks-proxy.net/',
            'https://www.sslproxies.org/'
        ],
        'enable': 0,
    },
    {
        'name': 'atomintersoft',
        'url_format': [
            'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
            'http://www.atomintersoft.com/anonymous_proxy_list',
        ],
        'enable': 0,
    },
    {
        'name': 'rmccurdy',
        'url_format': [
            'https://www.rmccurdy.com/scripts/proxy/good.txt'
        ],
        'enable': 0,
    },
    {
        'name': 'proxylistplus',
        'url_format': [
            'http://list.proxylistplus.com/Socks-List-1',
            'http://list.proxylistplus.com/SSL-List-1'
        ],
        'task_type': SPIDER_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'gatherproxy',
        'url_format': [
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
        'task_type': SPIDER_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'proxy-list',
        'url_format': [
            'https://proxy-list.org/english/index.php?p={}',
        ],
        'start':1,
        'end': 10,
        'task_type': SPIDER_AJAX_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'cnproxy',
        'url_format': [
            'http://www.cnproxy.com/proxy{}.html',
            'http://www.cnproxy.com/proxyedu{}.html'
        ],
        'start': 1,
        'end': 2,
        'task_type': SPIDER_AJAX_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'free-proxy',
        'url_format': [
            'http://free-proxy.cz/en/proxylist/main/{}',
        ],
        'start': 1,
        'end': 100,
        'task_type': SPIDER_AJAX_GFW_TASK,
        'enable': 0,
    },
    {
        'name': 'cool-proxy',
        'url_format': [
            'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:{}',
        ],
        'start': 1,
        'end': 10,
        'task_type': SPIDER_AJAX_TASK,
        'enable': 0,
    },
    {
        'name': 'mrhinkydink',
        'url_format': ['http://www.mrhinkydink.com/proxies.htm'] +
                      ['http://www.mrhinkydink.com/proxies%s.htm' % i for i in range(2, 10)]
        ,
        'enable': 0,
    },
    {
        'name': 'xroxy',
        'url_format': [
            'http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&sort=reliability'
            '&desc=true&pnum={}#table',
        ],
        'task_type': SPIDER_GFW_TASK,
        'start':0,
        'end': 5,  # max 100
        'enable': 0,
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
