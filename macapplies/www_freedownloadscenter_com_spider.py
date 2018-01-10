#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwFreedownloadscenterComSpider(scrapy.Spider):
    name="www_freedownloadscenter_com_spider"

    #start_urls=["http://freedownloadscenter.com/mac/"]

    def start_requests(self):
        pres_urls=["http://freedownloadscenter.com/mac/audio-and-video/",
                   "http://freedownloadscenter.com/mac/games/",
                   "http://freedownloadscenter.com/mac/system-tools/",
                   "http://freedownloadscenter.com/mac/design-and-photo/",
                   "http://freedownloadscenter.com/mac/mobile-phone-utilities/",
                   "http://freedownloadscenter.com/mac/developer-tools/",
                   "http://freedownloadscenter.com/mac/business/",
                   "http://freedownloadscenter.com/mac/internet-tools/",
                   "http://freedownloadscenter.com/mac/communication/",
                   "http://freedownloadscenter.com/mac/productivity/"
                   ]
        for each_pres_url in pres_urls:
            #print each_pres_url

            yield SplashRequest(url=each_pres_url,callback=self.parse)

    def parse(self, response):
        print response.url
        # s="http://freedownloadscenter.com/mac/audio-and-video/"

        # categories=response.xpath('/html/body/div[2]/div[1]/div/aside/div/ul/li/a/@href').extract()
        # print categories
        #
        # for each_category in categories:
        #     each_category_url="http:"+each_category
        #     print each_category_url

