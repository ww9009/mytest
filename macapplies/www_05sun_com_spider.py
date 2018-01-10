#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class Www05sunComSpider(scrapy.Spider):

    #start_urls=["http://www.05sun.com/apple/r_13_1.html"]
    name = "www_05sun_com_spider"
    base_url="http://www.05sun.com"
    #start_urls=["http://www.05sun.com/downinfo/68952.html"]

    # def start_requests(self):
    #     pres_url="http://www.05sun.com/downinfo/107540.html"
    #     yield SplashRequest(url=pres_url,callback=self.parse)
    #
    #
    # def parse(self, response):
    #     downlaod_url=response.xpath('//*[@id="info"]/a/@href').extract()
    #     # content=response.body
    #     #
    #     # pattern=re.compile(r'<span id="m_address".*style="display:none;">(.*)？</span>')
    #
    #     # res=pattern.findall(content)
    #     #print res
    #     print downlaod_url


    def start_requests(self):
        for i in range(1,253):
            page_url="http://www.05sun.com/apple/r_13_"+str(i)+".html"
            yield scrapy.Request(url=page_url,callback=self.parse)

    def parse(self, response):
        page_all_download_links = response.xpath('//body//div[@class="ls-list ov ti m15"]/div/a/@href').extract()
        #f=open("tmp2.txt",'a+')

        for each_download_link in page_all_download_links:
            each_download_url = self.base_url + each_download_link
            # print each_download_url
            # f.write(each_download_url+"\n")

            yield SplashRequest(url=each_download_url,callback=self.pres_each_download_url)
            #yield scrapy.Request(url=each_download_url,callback=self.pres_each_download_url)

    def pres_each_download_url(self,response):
        download_url=response.xpath('//*[@id="m_address"]/text()').extract()
        for each_downlaod_url in download_url:
            print each_downlaod_url







