#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwCrskyComSpider(scrapy.Spider):
    name = "www_crsky_com_spider"
    start_urls=["http://www.crsky.com/"]
    base_url="http://www.crsky.com/"

    def parse(self, response):
        categories=response.xpath('//*[@id="crsky"]/div[1]/div[3]/ul/li/a/@href').extract()
        for category in categories[1:-1]:
            category_url=self.base_url+category

            yield scrapy.Request(url=category_url,callback=self.parse_each_category)


    def parse_each_category(self,response):
        tmp_category_pages=response.xpath('//div[@class="pagination"]/a/@href').extract()[-2]

        tmp_total_pages=tmp_category_pages.split('_')[-1]
        total_pages=tmp_total_pages.split('.')[0]
        for i in range(1,int(total_pages)+1):

            tmp_url=response.url.split('.html')[0]
            tmp_url_2 = tmp_url.split('_')
            pres_url= tmp_url_2[0] + '_' + tmp_url_2[1] + '_'+str(i) + ".html"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        pass






