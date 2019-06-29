这篇文章的目的是阐述[haipproxy](https://github.com/ResolveWang/haipproxy)的主要架构和流程。该项目关键部分是
- 基于Scrapy和Redis的分布式爬虫，用作IP抓取和校验，对应于项目的[crawler](https://github.com/ResolveWang/haipproxy/tree/master/crawler)
- 基于Redis实现的分布式任务调度工具，对应于项目的[scheduler](https://github.com/ResolveWang/haipproxy/blob/master/scheduler)和[redis_util.py](https://github.com/ResolveWang/haipproxy/blob/master/utils/redis_util.py)

*Crawler*分为代理抓取和校验，两者实现思想类似，主要使用Scrapy的`spider_idle`信号和`DontCloseSpider`异常来阻止Scrapy在没有数据的时候关闭，灵感来自[scrapy-redis](https://github.com/rmax/scrapy-redis)。为了方便阐述，我画了一张包含各个组件的流程图，如下

![haipproxy workflow](../static/workflow.png)

- 启动调度器，包括代理爬虫调度器和校验爬虫调度器。调度器会读取[rules.py](https://github.com/ResolveWang/haipproxy/blob/master/config/rules.py)中待抓取的网站，将其编排成任务存入各个任务队列中
- 启动各个爬虫，包括IP抓取和校验程序。项目中爬虫和调度器都是高可用的，可以根据实际情况进行分布式部署，无需改动代码。由于本文的目标不是写成该项目的详细使用文档，所以省略了如指定启动爬虫类型和调度器类型的介绍
- 代理IP采集爬虫启动后会到对应的任务队列中获取任务并执行，再把获取到的结果存入一个`init`队列中
- `init`队列由一个特殊的校验器`HttpbinInitValidator`进行消费，它会过滤掉透明代理，再把可用代理输入各个`Validated`队列中
- 调度器会定时从`Validated`队列中获取代理IP，再将其存入一个临时的队列。这里用一个临时队列是为了让校验更加公平，如果直接从`Validated`队列中获取资源进行校验，那么会增大不公平性
- 这时候各个校验器(非`init`校验器)会从对应的临时队列中获取待校验的IP并对其进行校验，此处省略校验细节
- 校验完成后再将其放回到`Validated`队列中，等待下一轮校验
- 请求成功率(体现为分数)、响应速度和最近校验时间满足[settings.py](https://github.com/ResolveWang/haipproxy/blob/master/config/settings.py)所配置要求的代理IP将会被爬虫客户端所消费
- 为了屏蔽各个调用语言的差异性，目前实现的客户端是`squid`客户端，它可以作为爬虫客户端的中间件

到此，整个流程便完了。