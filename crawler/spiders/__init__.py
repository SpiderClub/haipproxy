"""
All the spiders crawl only anonymous ip.
Here are all the ip proxy website

website for common spider:
https://www.kuaidaili.com/
http://www.kxdaili.com/
http://www.nianshao.me/
http://www.xicidaili.com/
http://www.66ip.cn/

website for ajax spider:
http://www.goubanjia.com/
http://www.xdaili.cn/freeproxy
"""
from .basic_spider import CommonSpider
from .ajax_spider import AjaxSpider