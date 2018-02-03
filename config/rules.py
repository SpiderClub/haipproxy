"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""
from config.settings import (
    SPIDER_AJAX_TASK, SPIDER_GFW_TASK, SPIDER_AJAX_GFW_TASK)

# todo: consider incremental crawling and incremental parser
# todo: conbined the url of the same domain/according to spider type
# todo: crawl each website according their own timer scheduler
URLS = [
    # {
    #     'name': 'xici',
    #     'url_format': ['http://www.xicidaili.com/nn/%s' % i for i in range(1, 6)] +
    #                   ['http://www.xicidaili.com/wn/%s' % i for i in range(1, 6)] +
    #                   ['http://www.xicidaili.com/wt/%s' % i for i in range(1, 6)]
    #     ,
    #     'enable': 1
    #     # 每隔一个小时抓一次
    # },
    # {
    #     'name': 'kuaidaili',
    #     'url_format': ['https://www.kuaidaili.com/free/inha/%s' % i for i in range(1, 6)] +
    #                   ['https://www.kuaidaili.com/proxylist/%s' % i for i in range(1, 11)],
    #     'enable': 1
    #     # 每隔一个小时抓一次
    # },
    # {
    #     'name': 'kxdaili',
    #     'url_format': [
    #         'http://www.kxdaili.com/dailiip/%s/%s.html#ip' % (i, j) for i in range(1, 3) for j in range(1, 11)
    #     ],
    #     'enable': 0
    #     # 每隔一个小时抓一次
    # },
    # {
    #     'name': 'nianshao',
    #     'url_format': ['http://www.nianshao.me/?stype=1&page=%s' % i for i in range(1, 11)] +
    #                   ['http://www.nianshao.me/?stype=2&page=%s' % i for i in range(1, 11)] +
    #                   ['http://www.nianshao.me/?stype=5&page=%s' % i for i in range(1, 11)],
    #     'enable': 1
    #     # 每隔一个小时抓一次
    # },
    # {
    #     'name': 'xdaili',
    #     'url_format': ['http://www.xdaili.cn:80/ipagent/freeip/getFreeIps?page=1&rows=10'],
    #     'enable': 1,
    #     # 每十分钟抓一次
    # },
    # {
    #     'name': 'goubanjia',
    #     'url_format': ['http://www.goubanjia.com/free/gngn/index%s.shtml' % i for i in range(1, 11)] +
    #                   ['http://www.goubanjia.com/free/gwgn/index%s.shtml' % i for i in range(1, 11)],
    #     'task_type': SPIDER_AJAX_TASK,
    #     'enable': 1,
    #     # 每十分钟抓一次
    # },
    # {
    #     'name': '66ip',
    #     'url_format': ['http://www.66ip.cn/%s.html' % i for i in range(1, 3)] +
    #                   ['http://www.66ip.cn/areaindex_%s/%s.html' % (i, j)
    #                    for i in range(1, 35) for j in range(1, 3)],
    #
    #     'enable': 1
    #     # 两个小时抓一次
    # },
    # {
    #     'name': 'baizhongsou',
    #     'url_format': ['http://ip.baizhongsou.com/'],
    #     'enable': 1
    #     # 三十分钟抓一次
    # },
    # {
    #     # there are some problems using crawlspider, so we use basic spider
    #     'name': 'coderbusy',
    #     'url_format': ['https://proxy.coderbusy.com/'] +
    #                   ['https://proxy.coderbusy.com/classical/https-ready.aspx?page=%s' % i for i in range(1, 21)] +
    #                   ['https://proxy.coderbusy.com/classical/post-ready.aspx?page=%s' % i for i in range(1, 21)] +
    #                   ['https://proxy.coderbusy.com/classical/anonymous-type/anonymous.aspx?page=%s'
    #                    % i for i in range(1, 6)] +
    #                   ['https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page=%s'
    #                    % i for i in range(1, 6)] +
    #                   ['https://proxy.coderbusy.com/classical/country/cn.aspx?page=%s' % i for i in range(1, 21)] +
    #                   ['https://proxy.coderbusy.com/classical/country/us.aspx?page=%s' % i for i in range(1, 11)] +
    #                   ['https://proxy.coderbusy.com/classical/country/id.aspx?page=%s' % i for i in range(1, 6)] +
    #                   ['https://proxy.coderbusy.com/classical/country/ru.aspx?page=%s' % i for i in range(1, 6)],
    #     'enable': 1
    #     # 两个小时一次
    # },
    # {
    #     'name': 'data5u',
    #     'url_format': [
    #         'http://www.data5u.com/free/index.shtml',
    #         'http://www.data5u.com/free/gngn/index.shtml',
    #         'http://www.data5u.com/free/gwgn/index.shtml'
    #     ],
    #     'enable': 1,
    #     # 10分钟抓一次
    # },
    # {
    #     'name': 'httpsdaili',
    #     'url_format': ['http://www.httpsdaili.com/?stype=1&page=%s' % i for i in range(1, 8)],
    #     'enable': 1,
    #     # 三个小时抓一次
    # },
    # {
    #     'name': 'ip181',
    #     'url_format': ['http://www.ip181.com/'] +
    #                   ['http://www.ip181.com/daili/%s.html' % i for i in range(1, 4)],
    #     # 十分钟抓一次
    #     'enable': 1,
    # },
    # {
    #     'name': 'ip3366',
    #     'url_format': ['http://www.ip3366.net/free/?stype=1&page=%s' % i for i in range(1, 3)] +
    #                   ['http://www.ip3366.net/free/?stype=3&page=%s' % i for i in range(1, 3)],
    #     'enable': 1
    #     # 半个小时抓一次
    # },
    # {
    #     'name': 'iphai',
    #     'url_format': [
    #         'http://www.iphai.com/free/ng',
    #         'http://www.iphai.com/free/wg',
    #         'http://www.iphai.com/free/np',
    #         'http://www.iphai.com/free/wp',
    #         'http://www.iphai.com/'
    #     ],
    #     'enable': 1,
    #     # 一小时一次
    # },
    # {
    #     'name': 'swei360',
    #     'url_format': ['http://www.swei360.com/free/?page=%s' % i for i in range(1, 4)] +
    #                   ['http://www.swei360.com/free/?stype=3&page=%s' % i for i in range(1, 4)],
    #     'enable': 1,
    #     # 半个小时抓一次
    # },
    # {
    #     'name': 'yundaili',
    #     'url_format': [
    #         'http://www.yun-daili.com/free.asp?stype=1',
    #         'http://www.yun-daili.com/free.asp?stype=2',
    #         'http://www.yun-daili.com/free.asp?stype=3',
    #         'http://www.yun-daili.com/free.asp?stype=4',
    #     ],
    #     'enable': 1,
    #     # 六个小时抓一次
    # },
    # {
    #     'name': 'cn-proxy',
    #     'url_format': [
    #         'http://cn-proxy.com/',
    #         'http://cn-proxy.com/archives/218'
    #     ],
    #     'task_type': SPIDER_GFW_TASK,
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'proxydb',
    #     'url_format': ['http://proxydb.net/?offset=%s' % 15*i for i in range(20)],
    #     'task_type': SPIDER_AJAX_TASK,
    #     'enable': 1,
    #     # 3个小时抓一次
    # },
    # {
    #     'name': 'ab57',
    #     'url_format': [
    #         'http://ab57.ru/downloads/proxyold.txt',
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'proxylists',
    #     'url_format': [
    #         'http://www.proxylists.net/http_highanon.txt',
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'my-proxy',
    #     'url_format': [
    #         'https://www.my-proxy.com/free-elite-proxy.html',
    #         'https://www.my-proxy.com/free-anonymous-proxy.html',
    #         'https://www.my-proxy.com/free-socks-4-proxy.html',
    #         'https://www.my-proxy.com/free-socks-5-proxy.html'
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'us-proxy',
    #     'url_format': [
    #         'https://www.us-proxy.org/',
    #         'https://free-proxy-list.net/',
    #         'https://free-proxy-list.net/uk-proxy.html',
    #         'https://free-proxy-list.net/anonymous-proxy.html',
    #         'https://www.socks-proxy.net/',
    #         'https://www.sslproxies.org/'
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'atomintersoft',
    #     'url_format': [
    #         'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
    #         'http://www.atomintersoft.com/anonymous_proxy_list',
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'rmccurdy',
    #     'url_format': [
    #         'https://www.rmccurdy.com/scripts/proxy/good.txt'
    #     ],
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'proxylistplus',
    #     'url_format': [
    #         'http://list.proxylistplus.com/Socks-List-1',
    #         'http://list.proxylistplus.com/SSL-List-1'
    #     ],
    #     'task_type': SPIDER_GFW_TASK,
    #     'enable': 1,
    #     # 三个小时抓一次
    # },
    # {
    #     'name': 'gatherproxy',
    #     'url_format': [
    #         'http://www.gatherproxy.com/',
    #         'http://www.gatherproxy.com/proxylist/anonymity/?t=Elite',
    #         'http://www.gatherproxy.com/proxylist/anonymity/?t=Anonymous',
    #         'http://www.gatherproxy.com/proxylist/country/?c=China',
    #         'http://www.gatherproxy.com/proxylist/country/?c=Brazil',
    #         'http://www.gatherproxy.com/proxylist/country/?c=Indonesia',
    #         'http://www.gatherproxy.com/proxylist/country/?c=Russia',
    #         'http://www.gatherproxy.com/proxylist/country/?c=United%20States',
    #         'http://www.gatherproxy.com/proxylist/country/?c=Thailand',
    #         'http://www.gatherproxy.com/proxylist/port/8080',
    #         'http://www.gatherproxy.com/proxylist/port/3128',
    #         'http://www.gatherproxy.com/proxylist/port/80',
    #         'http://www.gatherproxy.com/proxylist/port/8118'
    #     ],
    #     'task_type': SPIDER_AJAX_GFW_TASK,
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'proxy-list',
    #     'url_format': ['https://proxy-list.org/english/index.php?p=%s' % i for i in range(1, 11)],
    #     'task_type': SPIDER_AJAX_GFW_TASK,
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'cnproxy',
    #     'url_format': ['http://www.cnproxy.com/proxy%s.html' % i for i in range(1, 11)] +
    #                   ['http://www.cnproxy.com/proxyedu%s.html' % i for i in range(1, 3)],
    #     'task_type': SPIDER_AJAX_GFW_TASK,
    #     'enable': 1,
    #     # 一个小时抓一次
    # },
    # {
    #     'name': 'free-proxy',
    #     'url_format': ['http://free-proxy.cz/en/proxylist/main/%s' % i for i in range(1, 30)],
    #     'task_type': SPIDER_AJAX_GFW_TASK,
    #     'enable': 1,
    #     # 三个小时抓一次
    # },
    # {
    #     'name': 'cool-proxy',
    #     'url_format': ['https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:1/page:%s'
    #                    % i for i in range(1, 11)],
    #     'task_type': SPIDER_AJAX_TASK,
    #     'enable': 1,
    #     # 半个小时抓一次
    # },
    # {
    #     'name': 'mrhinkydink',
    #     'url_format': ['http://www.mrhinkydink.com/proxies.htm']
    #     ,
    #     'enable': 1,
    #     # 两个小时抓一次
    # },
    # {
    #     'name': 'xroxy',
    #     'url_format': ['http://www.xroxy.com/proxylist.php?port=&type=&ssl=&country=&latency=&reliability=&'
    #                    'sort=reliability&desc=true&pnum=%s#table' % i for i in range(20)],
    #     'task_type': SPIDER_GFW_TASK,
    #     'enable': 0,
    #     # 一个小时抓一次
    # },
    {
        'name': 'mogumiao',
        'url_format': ['http://www.mogumiao.com/proxy/free/listFreeIp',
                       'http://www.mogumiao.com/proxy/api/freeIp?count=15'],
        'enable': 1,
        # 每五分钟抓一次
    },
]
