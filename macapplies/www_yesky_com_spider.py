#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwYeskyComSpider(scrapy.Spider):
    name="www_yesky_com_spider"
    start_urls=["http://mydown.yesky.com/mac"]

    def parse(self, response):
        pages=[1,3,2,5,3,2,1]
        categories=response.xpath('//*[@id="header"]/header/div[2]/ul[6]/li/a/@href').extract()

        for i  in range(len(categories)):
            #print categories[i]
            yield scrapy.Request(url=categories[i],callback=self.pres_each_category,meta={"pages":pages[i]})

    def pres_each_category(self,response):
        print response.url
        pages=response.meta["pages"]
        print pages
        for i in range(1,pages+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_url=response.url.split('.html')[0]
                pres_url=tmp_url+"_"+str(i)+".html"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):

        page_download_urls=response.xpath('//body//ul[@class="lh"]/li/div[1]/a/@href').extract()
        for each_download_url in page_download_urls:

            yield scrapy.Request(url=each_download_url,callback=self.get_each_download_url)

    def get_each_download_url(self,response):
        download_url=response.xpath('//body//ul[@class="bottom cl"]/li[1]/a/@href').extract()
        for each_download_url in download_url:
            item = CrawlmacappItem()
            item['soft_id'] = each_download_url
            item['soft_name'] = ""
            item['download_link'] = each_download_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item







