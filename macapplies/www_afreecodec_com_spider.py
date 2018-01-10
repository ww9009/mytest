#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwAfreecodecComSpider(scrapy.Spider):
    name = "www_afreecode_com_spider"

    def start_requests(self):
        urls=["http://mac.afreecodec.com/audio/","http://mac.afreecodec.com/video/"]
        pages=[52,85]
        for i in range(0,len(urls)):
            yield scrapy.Request(url=urls[i],callback=self.parse,meta={"Page":pages[i]})

    def parse(self, response):
        #print response.url
        pages=response.meta["Page"]
        #print pages
        for i in range(1,int(pages)+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+str(i)+".html"
            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)
    def pres_each_page(self,response):
        page_downlaod_urls=response.xpath('//body//ul[@class="listthree h90"]/li/p/a/@href').extract()
        for each_downlaod_url in page_downlaod_urls:
            #print each_downlaod_url
            yield scrapy.Request(url=each_downlaod_url,callback=self.pres_each_link)

    def pres_each_link(self,response):
        download_links=response.xpath('//body//div[@class="clearboth mb10"]/div[1]/span/a/@href').extract()
        for each_download_link in download_links:
            #print each_download_link
            yield scrapy.Request(url=each_download_link,callback=self.get_each_download_url)

    def get_each_download_url(self,response):
        download_urls=response.xpath('//body//div[@class="baseinfo"]/p/a/@href').extract()
        for each_downlaod_url in download_urls:

            item = CrawlmacappItem()
            item['soft_id'] = each_downlaod_url
            item['soft_name'] = ""
            item['download_link'] = each_downlaod_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item


