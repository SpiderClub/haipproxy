本文简要haipproxy支持的所有任务及其相关意义。

---

### 代理采集爬虫
代理采集爬虫相关实现见[crawler/spiders](https://github.com/SpiderClub/haipproxy/tree/master/crawler/spiders)部分

一共包含四种类型的爬虫

- `common`: 该类爬虫支持爬取普通类型的代理IP网站，即不需要做ajax渲染，也不需要翻墙的网站。

- `ajax`: 该类爬虫支持爬取需要ajax渲染的代理IP网站，需要安装[scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
并在设置里提供`SPLASH_URL`

- `gfw`: 该类爬虫用于爬取需要翻墙但是不需要ajax渲染的代理IP网站，需要在设置里提供`GFW_PROXY`，并且需要支持http协议

- `ajax_gfw`: 该类爬虫用于爬取需要翻墙同时也需要ajax渲染的代理IP网站，需要同时设置`GFW_PROXY`和`SPLASH_URL`

`haipproxy`支持通过启动命令来指定启动具体的爬虫实例，比如我们只想启动`common`和`ajax`相关的代理抓取爬虫，那么启动命令为
> python crawler_booter.py --usage crawler common ajax

同时，我们也可以在定时任务调度器中指定相关的定时任务
> python scheduler_booter.py --usage crawler common ajax

如果不指定具体的任务，默认会启动所有爬虫实例和定时任务调度

### 代理IP校验器
代理IP校验器具体实现见[crawler/validators](https://github.com/SpiderClub/haipproxy/tree/master/crawler/validators)

该类型的任务根据代理IP的具体用处可以进行定制，具体方法参考[针对特定站点添加校验器](https://github.com/SpiderClub/haipproxy/blob/master/docs/%E9%92%88%E5%AF%B9%E7%89%B9%E5%AE%9A%E7%AB%99%E7%82%B9%E6%B7%BB%E5%8A%A0%E6%A0%A1%E9%AA%8C%E5%99%A8.md)。
`haipproxy`默认支持的校验任务包括

- `init`: 该校验器的主要目的是对所有新采集到的ip进行初始校验，过滤掉透明IP并将代理IP放入后面需要使用的队列中

- `http`: 该校验器用于校验`http`代理，以[http://httpbin.org/ip](http://httpbin.org/ip)为校验对象，你也可以自己搭建相关的http校验站点

- `https`: 该校验器用于校验`https`代理，以[https://httpbin.org/ip](http://httpbin.org/ip)为校验对象，你也可以自己搭建相关的https校验站点

- `weibo`: 该校验器用于校验`weibo`的代理

- `zhihu`: 该校验器用于校验`zhihu`的代理

同样，`haipproxy`支持通过命令启动特定校验器的爬虫实例，比如我们只想`init`和`zhihu`的代理校验器，那么启动命令为
> python crawler_booter.py --usage validator init zhihu

同时，我们也可以在定时任务调度器中指定相关的定时任务
> python scheduler_booter.py --usage validator zhihu

不过需要注意两点

- `init`校验器属于特殊校验器，无论单机还是分布式部署`haipproxy`的时候，都必须启动至少一个`init`校验器实例。建议部署足够多的`init`校验器
实例，因为通过实践发现，一个`init`校验器往往不够用
- `init`校验器并没有相应的定时任务调度，它的资源获取是代理IP爬虫直接操作的


