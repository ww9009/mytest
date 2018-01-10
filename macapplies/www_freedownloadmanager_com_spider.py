#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwFreedownloadmanagerComSpider(scrapy.Spider):
    name="www_freedownloadmanager_com_spider"

    start_urls=["https://en.freedownloadmanager.org/Mac-OS/"]

    def parse(self, response):
        categories=response.xpath('//*[@id="category_list"]/li/a/@href').extract()
        for each_category in categories:
            each_category_url="https:"+each_category

            yield scrapy.Request(url=each_category_url,callback=self.pres_each_category)

    def pres_each_category(self,response):
        total_pages=34
        for i in range(1,total_pages+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_url=response.url.split('.htm')[0]
                pres_url=tmp_url+str(i)+".htm"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        download_attributes=response.xpath('//body//div[@class="prog_items"]/div[@class="prog_item"]/div[1]/@class').extract()
        download_links=response.xpath('//body/div[2]/div[4]/div/div[1]/div[1]/div/div/h3/a[1]/@href').extract()
        for i in range(len(download_attributes)):
            if download_attributes[i]=="prog_title prog_title_free":

                pres_url="https:"+download_links[i]

                yield scrapy.Request(url=pres_url,callback=self.get_each_download_url)
    def get_each_download_url(self,response):
        download_url=response.xpath('//body//div[@class="prog_download  "]/a/@href').extract()
        for each_download_url in download_url:
            each_download_url="https:"+each_download_url

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





