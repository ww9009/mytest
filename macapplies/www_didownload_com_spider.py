#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwDidownloadComSpider(scrapy.Spider):

    name = "www_didownlaod_com_spider"
    start_urls=["http://www.didown.com/"]
    base_url="http://www.didown.com"

    def parse(self, response):
        categories=response.xpath('//body/div/header/div[3]/ul/li/a/@href').extract()
        total_pages = [541, 545, 647, 449, 269, 120, 1404, 157, 91,737,121]
        used_categories=categories[:-1]
        for i in range(len(used_categories)):
            each_category_url=self.base_url+used_categories[i]

            yield scrapy.Request(url=each_category_url,callback=self.pres_each_category,meta={'total_page':total_pages[i]})

    def pres_each_category(self,response):
        category_pages=response.meta["total_page"]
        #print category_pages
        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_page_url=response.url
            else:
                pres_page_url=response.url+"/"+str(i)+".html"

            yield scrapy.Request(url=pres_page_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        page_download_links=response.xpath('//body//ul[@class="soft-list clearfix"]/li/div[1]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link

            yield scrapy.Request(url=each_download_url,callback=self.get_each_downlaod_url)

    def get_each_downlaod_url(self,response):
        this_platform=response.xpath('//body//ul[@class="soft-tech"]/li[7]/span/text()').extract()
        allow_platform="Mac"
        print this_platform

        if this_platform[0]==allow_platform:
            download_urls=response.xpath('//body//div[@class="down"]/dl/dd/a/@href').extract()
            for each_download_url in download_urls:
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






