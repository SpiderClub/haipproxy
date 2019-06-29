在[Readme](https://github.com/SpiderClub/haipproxy)中已经涉及到了haipproxy的使用方法，
由于篇幅所限，无法写得十分详细，所以这里专门用一篇文章来阐述它的部署和使用方式。

---

`haipproxy`只在Linux和Mac OS上做过测试，windows系统不保证程序的稳定运行。

## 服务端
### 单机部署
1.Python3和安装Redis。小白可以阅读[这篇文章](https://github.com/SpiderClub/weibospider/wiki/%E5%88%86%E5%B8%83%E5%BC%8F%E7%88%AC%E8%99%AB%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)
的相应部分来进行安装

2.根据`redis.conf`中对Redis做的设置修改[setting.py](https://github.com/SpiderClub/haipproxy/blob/master/config/settings.py)中`REDIS_HOST`和`REDIS_PASSWORD`等参数

3.安装Docker，根据[Docker官网的文档](https://docs.docker.com/install/)进行安装

4.安装[scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
  > docker run -p 8050:8050 -d --name mysplash --restart=always scrapinghub/splash
  然后根据实际情况配置文件[config/settings.py](config/settings.py)中的`SPLASH_URL`

5.安装项目相关依赖
  > pip install -r requirements.txt

6.启动*scrapy worker*，包括代理IP采集器和校验器
  > python crawler_booter.py --usage crawler

  > python crawler_booter.py --usage validator

  注意，我们可以只指定启动特定的代理IP采集器和校验器实例。
  代理IP采集器包括`common`、`ajax`、`gfw`和`ajax_gfw`四种任务。他们的具体意义和使用方法见[haipproxy中的任务类型和作用]()

7.启动*调度器*，包括代理IP定时调度和校验
  > python scheduler_booter.py --usage crawler

  > python scheduler_booter.py --usage validator

  注意，我们可以只启动特定的代理IP抓取调度器和校验调度器。具体操作请阅读[haipproxy中的任务类型和作用]()

### Docker部署
1.安装Docker，根据[Docker官网的文档](https://docs.docker.com/install/)进行安装

2.安装*docker-compose*
  > pip install -U docker-compose

3.根据配置文件的注释提示修改[settings.py](config/settings.py)中的`SPLASH_URL='http://splash:8050'`和`REDIS_HOST='redis'`参数

4.使用*docker-compose*启动各个应用组件
  > docker-compose up


### 集群部署
由于精力有限，目前只能通过手动部署`haipproxy`集群。部署方式并没有什么特别的，配置文件根据实际情况进行改动即可。无论是代理IP采集器、代理IP定时任务
调度器，还是代理IP校验器和代理IP校验定时任务调度器，都可以分布式部署到多台服务器上，并且可以根据实际情况，部署M:N的代理采集和校验节点。也可以在不同
爬虫节点上指定不同的任务，以充分利用服务器资源。由于实现了分布式锁，所以不用担心*scrapy worker*执行到重复的任务。

自动化部署方式笔者还需要继续考察，目前的思路有:
1.根据`scrapyd`来做集群部署
2.使用`ansible`做集群部署
3.使用`k8s`做集群部署

### 客户端

#### 调用Python客户端
示例代码见[examples/zhihu/](https://github.com/SpiderClub/haipproxy/blob/master/examples/zhihu/crawler.py)


#### 调用squid作为二级代理
1.安装squid，备份squid的配置文件并且启动squid，以ubuntu为例
  > sudo apt-get install squid

  > sudo sed -i 's/http_access deny all/http_access allow all/g'

  > sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.backup

  > sudo service squid start

2.根据操作系统修改项目配置文件[config/settings.py](config/settings.py)中的`SQUID_BIN_PATH`、
`SQUID_CONF_PATH`、`SQUID_TEMPLATE_PATH`等参数,参数的详细意义见[配置文件的参数和意义](https://github.com/SpiderClub/haipproxy/blob/master/docs/%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%8F%82%E6%95%B0%E5%92%8C%E6%84%8F%E4%B9%89.md)

3.启动`squid conf`的定时更新程序
  > sudo python squid_update.py

4.使用squid作为代理中间层请求目标网站,默认代理URL为'http://squid_host:3128',用Python请求示例如下
  ```python3
  import requests
  proxies = {'https': 'http://127.0.0.1:3128'}
  resp = requests.get('https://httpbin.org/ip', proxies=proxies)
  print(resp.text)
  ```

如果您使用的是项目提供的docker compose的方法，那么squid就不用安装了，直接就可以做请求