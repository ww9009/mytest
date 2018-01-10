#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwSoftsiloComSpider(scrapy.Spider):
    name = "www_softsilo_com_spider"
    base_url="http://www.softsilo.com"

    def start_requests(self):
        for i in range(1,282):
            if i==1:
                pres_url="http://www.softsilo.com/mac"
            else:
                pres_url="http://www.softsilo.com/mac/page-"+str(i)
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="main-wrapper-dark"]//div[@class="article-image"]/a/@href').extract()
        for each_download_url in page_download_links:
            yield scrapy.Request(url=each_download_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):
        download_links=response.xpath('//*[@id="main-wrapper-dark"]//div[@class="text-center"]/a/@href').extract()
        for each_download_link in download_links:
            each_download_url=self.base_url+each_download_link
            yield scrapy.Request(url=each_download_url,callback=self.get_each_download_url)

    def get_each_download_url(self,response):
        download_urls=response.xpath('//*[@id="download"]/@src').extract()
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

