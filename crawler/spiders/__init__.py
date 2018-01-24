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

website for ajax spider:
http://www.goubanjia.com/
http://www.xdaili.cn/freeproxy

website for crawl spider:
https://proxy.coderbusy.com/
http://proxydb.net/

website for gfw spider:
http://cn-proxy.com/

"""
from .basic_spider import CommonSpider
from .ajax_spider import AjaxSpider
from .crawl_spider import CrawlSpider
from .gfw_spider import GFWSpider