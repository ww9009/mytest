#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwCleansoftsComSpider(scrapy.Spider):
    name = "www_cleansofts_com_spider"
    base_url="http://cleansofts.org"

    def start_requests(self):
        for i in range(1,124):
            if i==1:
                pres_url="http://cleansofts.org/event/search.php?query=Mac"
            else:
                pres_url="http://cleansofts.org/event/search.php?query=Mac&start="+str(i)
            yield SplashRequest(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="content-left-in"]/table/tbody/tr/td/a/@href').extract()
        for each_download_link in page_download_links:
            #print each_download_link

            yield SplashRequest(url=each_download_link,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):
        download_links=response.xpath('//*[@id="overview"]/table/tbody/tr/td[1]/a/@href').extract()
        for each_download_url in download_links:
            yield SplashRequest(url=each_download_url,callback=self.get_each_download_url)

    def get_each_download_url(self,response):

        download_urls=response.xpath('//*[@id="overview"]/p/a[1]/@href').extract()
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



