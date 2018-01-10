#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwFindsoftwareComSpider(scrapy.Spider):
    name = "www_findsoftware_com_spider"
    base_url="http://www.findsoftware.eu"

    def start_requests(self):
        for i in range(1,4000):
            if i==1:
                pres_url="http://www.findsoftware.eu/"
            else:
                pres_url="http://www.findsoftware.eu/?page="+str(i)
            yield SplashRequest(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_downlaod_links=response.xpath('//*[@id="info"]/div[@class="post"]/table/tbody/tr/td[2]/a[2]/@href').extract()
        for each_download_link in page_downlaod_links:
            each_download_url=self.base_url+each_download_link

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

