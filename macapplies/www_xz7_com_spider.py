#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwXz7ComSpider(scrapy.Spider):
    name = "www_xz7_com_spider"
    base_url="http://www.xz7.com"
    use_url="http://www.xz7.com/zhuanti/318_1.htm"
    #start_urls=["http://www.xz7.com/zhuanti/318_1.htm"]


    def start_requests(self):
        total_page = 108
        for i in range(1, total_page + 1):
            pres_url = "http://www.xz7.com/zhuanti/318_" + str(i) + ".htm"
            yield SplashRequest(url=pres_url,callback=self.parse)
    def parse(self, response):
        #print response.url

        all_download_links = response.xpath('//*[@id="list_content"]/div/a/@href').extract()
        for each_downlaod_link in all_download_links:
            each_downlaod_url = self.base_url + each_downlaod_link
            #print each_downlaod_url
            yield SplashRequest(url=each_downlaod_url,callback=self.pres_each_download_link)

    def pres_each_download_link(self,response):
        print response.url
        #platform_info=response.xpath('//*[@id="c_soft_down"]/div[1]/ul[1]/li[2]/strong[2]').extract()
        #print platform_info
        download_url=response.xpath('//*[@id="download"]/div[1]/ul/li[1]/a/@href').extract()
        print download_url










