"""
All the spiders crawl only anonymous ip.
Here are all the ip proxy website

website for common spider:
https://www.kuaidaili.com/
http://www.kxdaili.com/
http://www.nianshao.me/
http://www.xicidaili.com/
http://www.66ip.cn/
http://www.data5u.com/
http://www.httpsdaili.com/
http://www.ip181.com/

website for ajax spider:
http://www.goubanjia.com/
http://www.xdaili.cn/freeproxy

website for crawl spider:
https://proxy.coderbusy.com/

"""
from .basic_spider import CommonSpider
from .ajax_spider import AjaxSpider
from .crawl_spider import CrawlSpider