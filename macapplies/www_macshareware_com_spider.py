#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwMacsharewareComSpider(scrapy.Spider):
    name = "www_macshareware_com_spider"
    start_urls=["http://www.macshareware.com/"]
    base_url="http://www.macshareware.com"

    def parse(self, response):
        categories=response.xpath('//body//span[@class="categories_item"]/a/@href').extract()
        #categories.remove("/maccategory/servers","")
        for each_category in categories:
            each_category_url=self.base_url+each_category
            yield scrapy.Request(url=each_category_url,callback=self.parse_each_category)
    def parse_each_category(self,response):
        category_pages=response.xpath('//body//div[@class="pager_left"]/a/text()').extract()
        if len(category_pages)==0:
            category_pages=1
        else:
            category_pages=category_pages[-2]
        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+"/"+str(i)

            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)
    def parse_each_page(self,response):

        page_downlaod_links=response.xpath('//body//div[@class="new_downloads blocks"]//div[@class="button_downl"]/a/@href').extract()
        for each_downlaod_link in page_downlaod_links:
            each_downlaod_url=self.base_url+each_downlaod_link
            try:
                yield scrapy.Request(url=each_downlaod_url,callback=self.parse_each_downlaod_link)
            except Exception,e:
                pass

    def parse_each_downlaod_link(self,response):
        print response.url
        downlaod_urls=response.xpath('//body//div[@align="center"]/a/@href').extract()
        for each_download_url in downlaod_urls:
            each_download_url=self.base_url+each_download_url

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



