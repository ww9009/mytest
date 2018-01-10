#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwDownload4yuComSpider(scrapy.Spider):
    name = "www_download4yu_com_spider"

    def start_requests(self):
        for i in range(1,303):
            if i==1:
                pres_url="http://www.download4you.com/php/search.php?key=Mac&category=All&range=Keywords&order=Downloads&x=0&y=0"
            else:
                pres_url="http://www.download4you.com/php/search.php?key=Mac&range=Keywords&category=All&order=Downloads&perpage=10&page="+str(i)
            yield SplashRequest(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_urls=response.xpath('//body//table/tbody/tr/td[2]/div[5]/center/table/tbody/tr/td/a/@href').extract()
        for each_download_url in page_download_urls:
            yield SplashRequest(url=each_download_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):

        download_urls=response.xpath('//body//center/table/tbody/tr[12]/td/b/font/a/text()').extract()
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

