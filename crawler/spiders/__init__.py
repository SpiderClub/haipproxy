"""
All the spiders crawl only anonymous ip.
Here are all the ip proxy website

website for common spider:
http://www.xicidaili.com/
https://www.kuaidaili.com/
http://www.kxdaili.com/
http://www.nianshao.me/
http://www.66ip.cn/
http://ip.baizhongsou.com/
http://www.data5u.com/
http://www.httpsdaili.com/
http://www.ip181.com/
http://www.ip3366.net/
http://www.iphai.com/
http://www.yun-daili.com/
http://ab57.ru/downloads/proxyold.txt
https://www.my-proxy.com/
https://www.us-proxy.org/
http://www.proxylists.net/http_highanon.txt
http://www.atomintersoft.com/
https://www.rmccurdy.com/scripts/proxy/good.txt
https://list.proxylistplus.com
http://www.mrhinkydink.com/proxies.htm
https://proxy.coderbusy.com/
http://www.mogumiao.com/

website for ajax spider:
http://www.goubanjia.com/
http://www.xdaili.cn/freeproxy
https://www.cool-proxy.net
http://proxydb.net/

website for gfw spider:
http://cn-proxy.com/
http://www.xroxy.com/

website for ajax gfw spider:
https://proxy-list.org/english/index.php
http://www.cnproxy.com/
http://free-proxy.cz/en/

"""
from .common_spider import CommonSpider
from .ajax_spider import AjaxSpider
from .gfw_spider import GFWSpider
from .ajax_gfw_spider import AjaxGFWSpider

# todo 有问题的 gather 66