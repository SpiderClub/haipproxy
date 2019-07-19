"""
All the spiders crawl only anonymous ip.
Here are all the ip proxy website

website for common spider:
http://ab57.ru/downloads/proxyold.txt
http://ip.baizhongsou.com/
http://www.66ip.cn/
http://www.atomintersoft.com/
http://www.data5u.com/
http://www.httpsdaili.com/
http://www.ip181.com/
http://www.ip3366.net/
http://www.iphai.com/
http://www.kxdaili.com/
http://www.mogumiao.com/
http://www.mrhinkydink.com/proxies.htm
http://www.nianshao.me/
http://www.proxylists.net/http_highanon.txt
http://www.xicidaili.com/
http://www.yun-daili.com/
https://list.proxylistplus.com
https://www.kuaidaili.com/
https://www.my-proxy.com/
https://www.rmccurdy.com/scripts/proxy/good.txt
https://www.us-proxy.org/

website for ajax spider:
http://proxydb.net/
http://www.goubanjia.com/
https://proxy.coderbusy.com/
https://www.cool-proxy.net

website for gfw spider:
http://cn-proxy.com/
http://www.xroxy.com/
https://free-proxy-list.net/

website for ajax gfw spider:
http://free-proxy.cz/en/
http://www.cnproxy.com/
https://proxy-list.org/english/index.php

"""
# todo find why 504 happens when crawling proxydb.net
from .ajax_spider import AjaxSpider, AjaxGFWSpider, GFWSpider
from .base import BaseSpider
from .common_spider import ProxySpider
from .validator import CctvValidator, HttpbinValidator, UqerValidator

all_spiders = [
    ProxySpider,
    AjaxSpider,
    GFWSpider,
    AjaxGFWSpider,
    CctvValidator,
    HttpbinValidator,
    UqerValidator,
]
