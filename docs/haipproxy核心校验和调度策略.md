昨日使用[haipproxy](https://github.com/SpiderClub/haipproxy)作为代理源，对`知乎`进行了数据抓取相关的性能测试，测试效果还不错，有兴趣的可以点击[项目主页](https://github.com/SpiderClub/haipproxy)查看测试结果。但是它仍有继续优化的空间，所以笔者打算单独写一篇文章来单独阐述它现有的IP筛选策略，也就是题目说的`高可用`策略。而关于部署的高可用后续文章会谈及到，这里暂时按下不表。

下文主要会谈到校验器和客户端的IP筛选策略。

---
### 校验器

我们知道，一个代理IP有多个属性，比如成功请求率、响应速度、是否支持Get/Post方法、是否匿名和该IP所处位置等。这些往往也是衡量一个IP质量的可参照标准。而从互联网上采集的免费IP大多数是短效的，所以代理IP对应的最近验证时间也是一个很重要的参考标准。[haipproxy](https://github.com/SpiderClub/haipproxy)目前主要参照`请求成功率`、`响应速度`、`最近验证时间`和`是否匿名`这四个维度对代理IP进行筛选。精力所限，目前还未打算对IP位置进行完善，而IP位置对于已登录的账户来说具有比较重要的意义。还有一点是，对于同一个代理IP，代理不同网站的效果可能大不相同，所幸的是，`haipproxy`可以[根据自己需求定制校验器](https://github.com/SpiderClub/haipproxy/blob/master/docs/%E9%92%88%E5%AF%B9%E7%89%B9%E5%AE%9A%E7%AB%99%E7%82%B9%E6%B7%BB%E5%8A%A0%E6%A0%A1%E9%AA%8C%E5%99%A8.md)

根据[haipproxy架构篇](https://github.com/SpiderClub/haipproxy/blob/master/docs/haipproxy%E6%9E%B6%E6%9E%84%E5%8F%8A%E6%B5%81%E7%A8%8B%E8%AF%B4%E6%98%8E.md)的介绍，我们可以知道`haipproxy initvalidator`会过滤掉部分透明的代理ip，另外一个过滤透明IP的地方是[proxy spiders](https://github.com/SpiderClub/haipproxy/tree/master/crawler/spiders)，它在抓取代理IP的时候会直接丢弃透明代理IP。因此，`是否匿名`这个标注我们已经实现了，后续所有的`validated queues`中存储的都是匿名及高匿IP。

`请求成功率`是以打分的方式来做的，这样做的原因是不需要对历时成功请求次数和失败请求次数进行记录和计算，优化了部分性能，又可以体现一个IP的稳定性。
那么打分的标准又是怎样的呢？`haipproxy`会先给定一个初始分数(5)。当成功一次，我们就对该代理加1分，为了防止分数短时间急剧增大，在分数大于一定阈值(10)后就对其进行更平滑的加分处理，具体为`round(10/score, 2)`，这样，分数会越来越难升高，但是足够衡量每个代理IP的稳定性了。当失败一次，就要分情况处理了。我们知道，很多免费代理IP可能短时间失效，比如代理端口被关了。这种情况下，`haipproxy`会直接丢弃该代理IP，因为它没有继续校验的必要性了，再对它进行校验只会增加校验器的负担。但是如果本次校验超时了，校验器会将该代理IP减一分，直到分数为0，则删除。对于不同分数的IP的选取会在客户端部分进行说明。

`响应速度`这个标准比较容易评判，`haipproxy`的做法是为校验器爬虫加载一个[profilemiddleware](https://github.com/SpiderClub/haipproxy/blob/master/crawler/middlewares.py)，从而获取到请求成功的代理IP的响应时间。同理，最近校验时间也比较容易获取到，我们使用redis的`zset`数据结构来存储它。

### 客户端
目前，`haipproxy`实现了两种形式的客户端：[squid](https://github.com/SpiderClub/haipproxy/blob/master/client/squid.py)和[py_cli](https://github.com/SpiderClub/haipproxy/blob/master/client/py_cli.py)。前者是语言无关的，它[使用squid作为二级代理](https://rookiefly.cn/detail/192)，它会定时自动更新squid配置文件，以获取新的可用代理，获取的方法和使用`py_cli`相同，下面会讲到。使用squid作为二级代理的好处是便于服务化，同时是语言无关的，我们的爬虫端只需要将代理设置为`http://squid_host:3128`就可以了，不用关心其它，但是这么做有一点不好的是，它的调度是轮询IP，并且对于不可用或者低质量IP的处理和反馈是不透明的。基于这点，有必要实现基于不同语言的客户端。

[py_cli](https://github.com/SpiderClub/haipproxy/blob/master/client/py_cli.py)是`haipproxy`代理获取的python实现。挑选可用代理的具体做法如下:
- 根据[配置文件](https://github.com/SpiderClub/haipproxy/blob/master/config/settings.py)的设置分别从`validated_queue`、`ttl_queue`和`speed_queue`中挑选出满足配置参数需求的代理再对其求交集，参数默认值是`LOWEST_SCORE = 6`、`TTL_VALIDATED_RESOURCE = 2`和`LONGEST_RESPONSE_TIME = 10`，表示的意思是选择分数大于６且最近验证时间在２分钟以内且最长响应时间不超过10s的代理。这样可以对上述的各个标准做合理的保证。在上述挑选方式选出来的代理数量不足(`len(proxies) < len(pool)*2`)的时候，会放宽挑选要求，对速度和最近验证时间求交集，然后和成功率做并集。如果代理数量还不足，它还会放低要求，对满足最近验证时间和成功率的集合做并集。

- 在爬虫客户端调用`py_cli`的时候，代理客户端`ProxyFetcher`会首先调用`refresh()`方法，如果`ProxyFetcher`中的可用代理量不够，那么就会通过上一步的算法对IP池进行扩充，如果数量足够，那么就会根据代理的调度策略选取合适的IP进行使用。

- 目前共有两种代理调度策略。(1)轮询策略。代理池是一个队列结构，每次从队首拿一个IP进行使用，如果该IP请求成功，则放到队尾，如果不成功，则需要调用`ProxyFetcher`的`proxy_feedback()`方法将结果进行反馈。这种策略的好处是IP负载比较均衡。但是缺点在于，IP质量参差不齐，有的响应时间很快，有的响应时间很慢，并且高质量的免费代理IP的生命周期可能很短，这样就无法充分利用。(2)贪婪策略。使用此种策略的时候，需要爬虫端对每次请求的响应时间进行记录，每次使用后调用`proxy_feedback()`方法以决定该代理IP是否继续下一次请求的时候被使用。如果使用某个代理IP的响应时间低于传入的`response_time`参数，那么就会一直使用它，直到不能用就从代理池中删除。如果时间高于了`response_time`，那么它会把该IP放入队尾。概括起来，该策略就是**低质量IP轮询，高质量IP一直使用**。

---

上述便是目前关于[haipproxy](https://github.com/SpiderClub/haipproxy)的代理IP挑选策略的所有细节。如果项目对您有用，不妨在Github上给个star。