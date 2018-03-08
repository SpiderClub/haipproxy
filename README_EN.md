# HAipproxy
[中文文档](README.md) | [README](README_EN.md)

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

## Standalone

### Server
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


### Client
`haipproxy` provides both [py client](client/py_cli.py) and [squid proxy](squid_update.py) for your spiders.Any clients about any languages are welcome!

#### Python Client
```python3
from client.py_cli import ProxyFetcher
# args are used to connect redis, if args is None, redis args in settings.py will be used
args = dict(host='127.0.0.1', port=6379, password='123456', db=0)
# https is used for common proxy.If you want to crawl a customized website, you'd better 
# write a customized ip validator according to zhihu validator
fetcher = ProxyFetcher('https', strategy='greedy', length=5, redis_args=args)
# get one proxy ip
print(fetcher.get_proxy())
# get available proxy ip list
print(fetcher.get_proxies()) # or print(fetcher.pool)
```

#### Using squid as proxy server
- Install squid,copy it's conf as a backup and then start squid, take *ubuntu* for example
   > sudo apt-get install squid
   
   > sudo sed -i 's/http_access deny all/http_access allow all/g'
   
   > sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup
   
   > sudo service squid start
- Change `SQUID_BIN_PATH`,`SQUID_CONF_PATH` and `SQUID_TEMPLATE_PATH` in *[config/settings.py](config/settings.py)* according to your OS
- Update squid conf periodically
  > sudo python squid_update.py
- After a while,you can send requests with squid proxies, the proxies url is 'http://squid_host:3128', e.g.
  ```python3
  import requests
  proxies = {'https': 'http://127.0.0.1:3128'}
  resp = requests.get('https://httpbin.org/ip', proxies=proxies)
  print(resp.text)
  ```

## Dockerize
- Install Docker

- Install docker-compose
  > pip install -U docker-compose

- Change`SPLASH_URL`and`REDIS_HOST`in [settings.py](config/settings.py)
  ```python3
  SPLASH_URL = 'http://splash:8050'
  REDIS_HOST = 'redis'
  ```
- Start all the containers using docker-compose
  > docker-compose up

- Use [py_cli](client/py_cli.py) or Squid to get available proxy ips.
  ```python3
  from client.py_cli import ProxyFetcher
  args = dict(host='127.0.0.1', port=6379, password='123456', db=0)
  fetcher = ProxyFetcher('https', strategy='greedy', length=5, redis_args=args)
  print(fetcher.get_proxy())
  print(fetcher.get_proxies()) # or print(fetcher.pool)
  ```

or 

```python3
import requests
proxies = {'https': 'http://127.0.0.1:3128'}
resp = requests.get('https://httpbin.org/ip', proxies=proxies)
print(resp.text)
```

# WorkFlow
![](static/workflow.png)

# Other important things
- This project is highly dependent on redis,if you want to replace redis with another mq or database,
just do it at your own risk
- If there is no Great Fire Wall at your country,set`proxy_mode=0` in both [gfw_spider.py](crawler/spiders/gfw_spider.py) and [ajax_gfw_spider.py](crawler/spiders/ajax_gfw_spider.py).
If you don't want to crawl some websites, set `enable=0` in [rules.py](config/rules.py)
- Becase of the Great Fire Wall in China, some proxy ip may can't be used to crawl some websites.You can extend the proxy pool by yourself in [spiders](crawler/spiders)
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

