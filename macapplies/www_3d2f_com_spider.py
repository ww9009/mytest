#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class Www3d2fComSpider(scrapy.Spider):
    name = "www_3d2f_com_spider"
    base_url="http://3d2f.com"

    def start_requests(self):
        for i in range(1,101):
            if i==1:
                pres_url="http://3d2f.com/top/programs/freeware/mac/"
            else:
                pres_url="http://3d2f.com/top/programs/freeware/mac/page"+str(i)+"/"

            yield SplashRequest(url=pres_url,callback=self.parse)
    def parse(self, response):
        page_downlaod_links=response.xpath('/html/body/table/tbody/tr[1]/td[3]/a[2]/@href').extract()
        for each_download_link in page_downlaod_links:
            each_download_url=self.base_url+each_download_link

            yield SplashRequest(url=each_download_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):
        #print response.url

        download_urls=response.xpath('/html/body/p/a/@href').extract()

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