#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwAllsoftwaresComSpider(scrapy.Spider):
    name = "www_allsoftwares_com_spider"
    base_url="http://mac.en.all-softwares.com"

    def start_requests(self):
        for i in range(1,245):
            if i==1:
                pres_url="http://mac.en.all-softwares.com/"
            else:
                pres_url="http://mac.en.all-softwares.com/"+str(i)
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="download"]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            yield scrapy.Request(url=each_download_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):

        download_urls=response.xpath('//*[@id="downloadbtn"]/@href').extract()
        for each_download_url in download_urls:
            items = CrawlmacappItem()
            items['soft_id'] = each_download_url
            items['soft_name'] = ''
            items['download_link'] = each_download_url
            items['is_download'] = False
            items['download_time'] = ""
            items['is_upload_ftp'] = False
            items['upload_time'] = ""
            items['upload_file_name'] = ""
            items['download_http_error'] = False
            items['soft_desc'] = ""
            yield items

