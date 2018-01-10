#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwDownloadtyphoonComSpider(scrapy.Spider):
    name = "www_downloadtyphoon_com_spider"
    base_url="https://www.downloadtyphoon.com"

    def start_requests(self):
        for i in range(1,307):
            if i==1:
                pres_url="https://www.downloadtyphoon.com/software-search.html?keywords=Mac"
            else:
                pres_url="https://www.downloadtyphoon.com/downloads/mac/"+str(25*(i-1))
            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)

    def parse_each_page(self,response):

        page_download_urls=response.xpath('//*[@id="right_col"]/div/div/a[1]/@href').extract()
        for each_download_url in page_download_urls:
            yield scrapy.Request(url=each_download_url,callback=self.parse_each_download_url)

    def parse_each_download_url(self,response):
        download_urls=response.xpath('//*[@id="right_col"]/div[2]/div/div/p/a/@href').extract()
        for each_download_url in download_urls:
            each_download_url=self.base_url+each_download_url

            #if each_download_url.endswith(".exe")==0:

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




