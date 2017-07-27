【环境】python 2.7 scrapy 1.4 PhantomJS Pyodbc sqlserver 2008

采用PhantomJS 来获取js动态内容，虽然速度会相当慢，但是也是windows系统上不得已的选择。

网上谈到的方式也是五花八门，尝试了用scrapy-splash，据说速度可以，但是splash是基于docker容器的，windows上安装docker，问题层出不穷，最后还是放弃了。

这个爬虫速度是慢了一点，初步爬取300个新闻内容大概需要20多分钟，但还算稳定。