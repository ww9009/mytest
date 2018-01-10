#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwMaczappComSpider(scrapy.Spider):
    name="www_maczapp_com_spider"
    base_url="http://www.maczapp.com"

    def start_requests(self):
        for i in range(1,5651):
            if i==1:
                pres_url="http://www.maczapp.com/soft"
            else:
                pres_url="http://www.maczapp.com/soft-p-"+str(i)

            #print pres_url
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="popular"]/div/h3/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            print each_download_url

