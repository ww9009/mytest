#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwAskedfilesComSpider(scrapy.Spider):
    name = "www_askedfiles_com_spider"

    def start_requests(self):
        for i in range(1,827):
            pres_url="http://www.askedfiles.com/showpads.php?sort=Title&cat=All&search=Description&string=Mac&match=Any&page="+str(i)
            yield SplashRequest(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="right_content"]/table/tbody/tr/td/table/tbody/tr[5]/td/a/@href').extract()
        for each_download_url in page_download_links:
            if each_download_url.endswith('.exe')==0:

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




