# -*- coding: utf-8 -*-
# Author:   BinBin
# Email:    289594665@qq.com
# Time :    2017/07/27

import random

from scrapy import signals
from scrapy.http import HtmlResponse, Response
from selenium import webdriver

class ThirtySixSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        print "from_crawler"
        s = cls(crawler.settings.getlist('USER_AGENTS'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        print "process_spider_input"
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        print "process_spider_output"
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        print "process_spider_exception"

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        print "process_start_requests"
        for r in start_requests:
            #随机获取UserAgent
            r.headers.setdefault('User-Agent', random.choice(self.agents))
            yield r

    def spider_opened(self, spider):
        print "spider_opened"
        spider.logger.info('Spider opened: %s' % spider.name)

class ThirtySixDownloaderMiddleware:

    @classmethod
    def process_request(cls, request, spider):
        #利用PhantomJS加载网页中的javascript动态内容
        print("ThirtySixDownloaderMiddleware")
        driver = webdriver.PhantomJS()
        driver.get(request.url)
        content = driver.page_source.encode('utf-8')
        #print content
        driver.quit()
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)