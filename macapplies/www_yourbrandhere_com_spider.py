#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwYoubrandhereComSpider(scrapy.Spider):
    name = "www_yourbrandhere_com_spider"

    s="http://padsites.org/site/ybh_software_download.html"
    def start_requests(self):
        for i in range(1,4622):
            if i==1:
                pres_url="http://ip-66-51-104-19.tera-byte.com/showpads.php?cat=All"
            else:
                pres_url="http://ip-66-51-104-19.tera-byte.com/showpads.php?sort=Title&cat=All&page="+str(i)
            #print pres_url
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        print(response.url)