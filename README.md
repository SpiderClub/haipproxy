# HAipproxy
本项目所采集的IP资源都来自互联网，由于网上代理IP资源的质量参差不齐，所以该项目应运而生了。
该项目的愿景是为大型爬虫项目提供一个**高可用低延迟的高匿HTTP/HTTPSIP代理池**。

# Features
- 快速抓取代理IP。项目使用scrapy做高速网络请求，能快速填充IP代理池
- IP抓取和提取精准。目前很多同类项目都是简单做的抓取，对于诸如[全网代理IP](http://www.goubanjia.com/free/gngn/index.shtml)
这类做了前端混淆的加密网站几乎没做还原处理。某些网站页面结构看似单一，却暗含陷阱。本项目有效地解决了这两个问题。
- IP来源丰富。本项目的IP来源参考了大量的同类开源项目（有兴趣可以查看`Reference`部分）。
造这个轮子的原因是别的项目大多数都做效果得让人不满意或是所用语言不相同，或是代码味道不好，强迫症患者看着很难受。
- 优良的IP校验器。使用复杂算法对IP进行建模及打分，从多个维度对代理IP进行校验，在高度不可用的代理IP资源中力求做到高可用。
- 优雅的编码设计和实现。项目使用Python编码，笔者力求用*Pythonic*的方式实现所有功能。笔者能力有限，有些地方实现还是比较
dirty，希望得到大神的指正。
- 支持高可用部署和抓取。爬虫任务调度器和Scrapy Worker都可以轻松进行水平扩展，无任何单点故障（消息和存储后端需要自己做高可用），
代码不需要进行任何改动。
- MIT授权协议。Just do whatever you want!

# Quick start

# How to contribute
- 欢迎给项目提新feature
- 如果发现项目任何地方实现不合理，或者还可以改进，欢迎提issue或者pr
- 如果你发现了比较好的代理网站，欢迎分享或者直接以PR的方式分享
- 如果在使用过程中发现项目哪个环节有问题，欢迎提issue


# Important things to notice
- 本项目高度依赖redis，除了消息通信和数据存储之外，IP校验使用了Redis中的多种数据结构。

# More docs for support

# Reference
本项目参考了Github上开源的各个爬虫代理的实现，感谢他们的付出，下面是笔者参考的所有项目，排名不分先后。

[dungproxy](https://github.com/virjar/dungproxy)

[proxyspider](https://github.com/zhangchenchen/proxyspider)

[ProxyPool](https://github.com/henson/ProxyPool)

[proxy_pool](https://github.com/jhao104/proxy_pool)

[ProxyPool](https://github.com/WiseDoge/ProxyPool)

[IPProxyTool](https://github.com/awolfly9/IPProxyTool)

[IPProxyPool](https://github.com/qiyeboy/IPProxyPool)

[proxy_list](https://github.com/gavin66/proxy_list)

[proxy_pool](https://github.com/lujqme/proxy_pool)