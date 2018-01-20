"""
Spider rules.Scheduler will provide crawling tasks according to the rules and
spiders will parse response content according to the rules.
"""


# todo: consider incremental crawling and incremental parser
# todo: consider filter transport ip
# todo: consider use socks5 to crawl the website outsite the wall
URLS = [
    {
        'name': 'xici',
        'url_format': 'http://www.xicidaili.com/nn/{}',
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'kuaidaili',
        'url_format': 'https://www.kuaidaili.com/free/inha/{}',
        'start': 1,
        'end': 2,
        'enable': 0
    },
    {
        'name': 'goubanjia',
        'url_format': 'http://www.goubanjia.com/free/gngn/index{}.shtml',
        'start': 1,
        'end': 11,
        'enable': 1
    },
    {
        'name': 'goubanjia',
        'url_format': 'http://www.goubanjia.com/free/gngn/index{}.shtml',
        'start': 1,
        'end': 11,
        'enable': 1
    },
]

