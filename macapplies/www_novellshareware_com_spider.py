#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwNovellsharewareComSpider(scrapy.Spider):
    name = "www_novellshareware_com_spider"
    start_urls=["http://mac.novellshareware.com/"]
    base_url="http://mac.novellshareware.com"


    def parse(self, response):
        categories=response.xpath('//*[@id="category"]/ul/li/ul/li/a/@href').extract()
        for each_category_url in categories:

            yield scrapy.Request(url=each_category_url,callback=self.parse_each_category)
    def parse_each_category(self,response):
        category_pages=response.xpath('//*[@id="content"]/div/div/div[1]/div[2]/a/text()').extract()[-2]
        #print response.url
        #print category_pages
        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_pres_url=response.url.split('.html')[0]
                pres_url=tmp_pres_url+"-page"+str(i)+".html"

            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)

    def parse_each_page(self,response):
        page_download_links=response.xpath('//body//div[@class="fright"]/a[2]/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link

            #re_download_url = requests.head(each_download_url, allow_redirects=True)

            item = CrawlmacappItem()
            item['soft_id'] = each_download_url
            item['soft_name'] = ""
            item['download_link'] = each_download_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""

            yield item






