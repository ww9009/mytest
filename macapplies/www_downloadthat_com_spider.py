#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwDownloadthatComSpider(scrapy.Spider):
    name = "www_download_com_spider"
    start_urls=["http://www.downloadthat.com/macintosh/"]
    base_url="http://www.downloadthat.com"

    def parse(self, response):
        categories=response.xpath('//*[@id="menu"]/ul[1]/li/ul/li/a/@href').extract()
        for each_category in categories:
            each_category_url=self.base_url+each_category
            try:
                yield scrapy.Request(url=each_category_url,callback=self.parse_each_category)
            except Exception,e:
                pass

    def parse_each_category(self,response):
        print response.url
        tmp_category_pages=response.xpath('//*[@id="content"]/div/div/div[24]/a/text()').extract()
        category_pages=tmp_category_pages[-2]

        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+"index"+str(i)+".html"
            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)
    def parse_each_page(self,response):
        page_download_links=response.xpath('//body//div[@class="gray"]//div[@class="row"]//strong[2]/a/@href').extract()
        for each_downlaod_link in page_download_links:
            each_downlaod_url=self.base_url+each_downlaod_link
            yield scrapy.Request(url=each_downlaod_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):
        #print response.url
        download_urls=response.xpath('//body//div[@align="center"]/strong[2]/a/@href').extract()
        for each_download_link in download_urls:
            each_download_url=self.base_url+each_download_link

            #re_download_url=requests.head(each_download_url,allow_redirects=True)
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





