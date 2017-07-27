# -*- coding: utf-8 -*-
# Author:   BinBin
# Email:    289594665@qq.com
# Time :    2017/07/27

import urllib2
import sys

import re
import scrapy
import logging

from pip._vendor.requests.packages import chardet
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from ..items import ArticleItem
from scrapy import Request
import logging

reload(sys)
sys.setdefaultencoding("utf-8")

class ThirtySixSpider(scrapy.Spider):
    name = "ThirtySix"
    allowed_domains = ["36kr.com"]
    start_urls = ['http://36kr.com']

    def parse(self, response):
        print "url:" + response.url
        print "response:" + response.__str__()

        links = response.xpath('//a[contains(@href, "/p/")]//@href').extract()

        #1、获取类似http://36kr.com/p/5055572.html这样的链接
        newsFullLinks = response.xpath('//a[re:test(@href, ".+(/p/\d+\.html)$")]/@href').extract()
        for link in newsFullLinks:
            yield Request(link, callback=self.parse_item)

        #2、获取类似/p/5084179.html这样的链接
        newsIncompleteLinks = response.xpath('//a[re:test(@href, "^(/p/\d+\.html)$")]/@href').extract()
        for link in newsIncompleteLinks:
            link = response.urljoin(link)
            #print link
            yield Request(link, callback=self.parse_item)

        # 3、获取/tags/***、/user/***、/topics/****这样的链接
        otherIncompleteLinks = response.xpath('//a[re:test(@href, "(^/tags/|^/user/|^/topics/).*")]/@href').extract()
        for link in otherIncompleteLinks:
            link = response.urljoin(link)
            #print link
            yield Request(link, callback=self.parse_next)

        # 3、获取http://36kr.com/tags/***、http://36kr.com/user/***、http://36kr.com/topics/****这样的链接
        otherFullLinks = response.xpath('//a[re:test(@href, "(^.+/tags/|^.+/user/|^.+/topics/).*")]/@href').extract()
        for link in otherFullLinks:
            #print link
            yield Request(link, callback=self.parse_next)

    #爬去下一个页面
    def parse_next(self, response):
        links = response.xpath('//a[contains(@href, "/p/")]//@href').extract()

        # 1、获取类似http://36kr.com/p/5055572.html这样的链接
        newsFullLinks = response.xpath('//a[re:test(@href, ".+(/p/\d+\.html)$")]/@href').extract()

        for link in newsFullLinks:
            yield Request(link, callback=self.parse_item)

        # 2、获取类似/p/5084179.html这样的链接
        newsIncompleteLinks = response.xpath('//a[re:test(@href, "^(/p/\d+\.html)$")]/@href').extract()
        for link in newsIncompleteLinks:
            link = response.urljoin(link)
            print link
            yield Request(link, callback=self.parse_item)

        # 3、获取/tags/***、/user/***、/topics/****这样的链接
        otherIncompleteLinks = response.xpath('//a[re:test(@href, "(^/tags/|^/user/|^/topics/).*")]/@href').extract()
        for link in otherIncompleteLinks:
            link = response.urljoin(link)
            #print link
            yield Request(link, callback=self.parse_next)

        # 3、获取http://36kr.com/tags/***、http://36kr.com/user/***、http://36kr.com/topics/****这样的链接
        otherFullLinks = response.xpath('//a[re:test(@href, "(^.+/tags/|^.+/user/|^.+/topics/).*")]/@href').extract()
        for link in otherFullLinks:
            #print link
            yield Request(link, callback=self.parse_next)

    #分析新闻内容
    def parse_item(self, response):

        print "parse_item url:" + response.url
        item = ArticleItem()

        article_titles = response.xpath('//div[re:test(@id, "J_post_wrapper_.*")]/div[1]/h1/text()').extract()
        if (article_titles.count > 0):
            print "article_title:" + article_titles[0]
            item["article_title"] = article_titles[0]

        article_authors = response.xpath('//div[re:test(@id, "J_post_wrapper_.*")]/div[1]/div[1]/div[contains(@class, "author-panel")]/div[contains(@class, "author")]/a/span/text()').extract()
        if (article_authors.count > 0):
            print "article_author:" + article_authors[0]
            item["article_author"] = article_authors[0]

        article_summarys = response.xpath('//div[re:test(@id, "J_post_wrapper_.*")]/div[1]/div[1]/section[@class="summary"]/text()').extract()
        print "article_summarys:" + article_summarys.__str__()
        if (article_summarys.count > 0):
            print "article_summary:" + article_summarys[0]
            item["article_summary"] = article_summarys[0]

        article_icons = response.xpath('//div[re:test(@id, "J_post_wrapper_.*")]/div[1]/div[1]/section[@class="headimg"]/img/@src').extract()
        print "article_icons:" + article_icons.__str__()
        if (article_icons.count > 0):
            print "article_icon:" + article_icons[0]
            item["article_icon"] = article_icons[0]

        article_contents = response.xpath('//div[re:test(@id, "J_post_wrapper_.*")]/div[1]/div[1]/div[2]/section').extract()
        print "article_contents:" + article_contents.__str__()
        if (article_contents.count > 0):
            print "article_content:" + article_contents[0]
            item["article_content"] = article_contents[0]

        item["article_url"] = response.url
        if (item["article_title"] is not None):
             yield item