# HAipproxy
[README](README.md) | [中文文档](README_ZH.md)

This project crawls proxy ip resources from the Internet.What we wish is to provide a 
anonymous ip proxy pool with **highly availability and low latency** for distributed 
spiders.

# Features
- Distributed crawlers with high performance, powered by scrapy and redis
- Large-scale of proxy ip resources
- HA design for both crawlers and schedulers
- Flexible architecture with task routing
- Support HTTP/HTTPS and Socks5 proxy
- MIT LICENSE.Feel free to do whatever you want

# Quick start

### Standalone
- Install Python3 and Redis Server
- Change redis args of the project *[config/settings.py](config/settings.py)* according to redis conf,such as `REDIS_HOST`,`REDIS_PASSWORD`
- Install [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) and change `SPLASH_URL` in *[config/settings.py](config/settings.py)*
- Install dependencies
  > pip install -r requirements.txt
- Start *scrapy worker*,including ip proxy crawler and validator
  > python crawler_booter.py --usage crawler

  > python crawler_booter.py --usage validator
- Start *task scheduler*,including crawler task scheduler and validator task scheduler
  > python scheduler_booter.py --usage crawler

  > python scheduler_booter.py --usage validator

### Dockerize
- Install docker-compose
  > pip install -U docker-compose

- Start all the containers using docker-compose
  > docker-compose up

# WorkFlow
![](static/workflow.png)

# Other important things
- This project is highly dependent on redis,if you want to replace redis with another mq or database,
just do it at your own risk
- If there is no Great Fire Wall at your country,set`proxy_mode=0` in both [gfw_spider.py](crawler/spiders/ajax_spider.py) and [ajax_gfw_spider.py](crawler/spiders/ajax_gfw_spider.py).
If you don't want to crawl some websites, set `enable=0` in [rules.py](config/rules.py)
- Issues and PRs are welcome
- Just star it if it's useful to you

# Reference
Thanks to all the contributors of the following projects.

[dungproxy](https://github.com/virjar/dungproxy)

[proxyspider](https://github.com/zhangchenchen/proxyspider)

[ProxyPool](https://github.com/henson/ProxyPool)

[proxy_pool](https://github.com/jhao104/proxy_pool)

[ProxyPool](https://github.com/WiseDoge/ProxyPool)

[IPProxyTool](https://github.com/awolfly9/IPProxyTool)

[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)

[proxy_list](https://github.com/gavin66/proxy_list)

[proxy_pool](https://github.com/lujqme/proxy_pool)

