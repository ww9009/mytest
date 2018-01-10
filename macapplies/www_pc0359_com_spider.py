#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwPc0359ComSpider(scrapy.Spider):
    name = "www_pc0359_com_spider"
    base_url="http://www.pc0359.cn"
    base_url2="http://www.pc0359.cn/mac/"
    start_urls=["http://www.pc0359.cn/mac/"]

    def parse(self, response):

        categories=response.xpath('//body//dd[@id="nav"]/a/@href').extract()
        for each_category in categories[1:]:
            each_category_url= self.base_url+each_category
            yield scrapy.Request(url=each_category_url,callback=self.pres_each_category)
    def pres_each_category(self,response):
        pattern = re.compile(r'(.*)-.*')
        tmp_total_pages=response.xpath('//body//dl[@id="mlist"]//div[@class="page-num"]/a[@class="last"]/text()').extract()[0]
        total_pages= tmp_total_pages[-2:]
        for i in range(1,int(total_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_1=a=response.url.split('/')[-1].split('.')[0]
                tmp_2 = pattern.findall(tmp_1)[0]
                pres_url=self.base_url2+tmp_2+"-"+str(i)+".html"

            print pres_url






