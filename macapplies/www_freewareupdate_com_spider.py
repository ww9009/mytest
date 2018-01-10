#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwFreewareupdateComSpider(scrapy.Spider):
    name="www_freewareupdate_com_spider"
    start_urls=["http://mac.freewareupdate.com/"]
    base_url="http://mac.freewareupdate.com"


    def parse(self, response):
        #print(response.url)
        categories=response.xpath('//*[@id="viewmore"]/a/@href').extract()
        for each_category in categories[2:]:
            yield scrapy.Request(url=each_category,callback=self.pres_each_category)

    def pres_each_category(self,response):
        #print(response.url)
        #print(response.body)

        dlurls=response.xpath('//body//div[@class="item column-1"]//td[@rowspan="4"]/a/@href').extract()
        for each_url in dlurls:
            each_download_url=self.base_url+each_url
            #print(each_download_url)
            yield SplashRequest(url=each_download_url,callback=self.pres_each_download_page)

    def pres_each_download_page(self,response):

        #print response.url
        for i in range(10000,10010):
            if i==10000:
                pres_url=response.url
            else:
                pres_url=response.url+"/"+str(i)+"/"
            try:
                yield SplashRequest(url=pres_url,callback=self.get_downlaod_url)
            except Exception,e:
                pass

    def get_downlaod_url(self,response):
        allow_postfix=('.dmg','.zip','.rar','.tar')
        downoad_urls=response.xpath('//*[@id="table-h1"]/tbody/tr/td[3]/table/tbody/tr/td/a/@href').extract()
        for each_download_url in downoad_urls:
            if each_download_url.endswith(allow_postfix):

                print each_download_url

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
            else:
                pass
                #yield SplashRequest(url=each_download_url,callback=self.get_redownload_url)

    def get_redownload_url(self,response):

        downlaod_urls=response.xpath('//table/tbody/tr/td[2]/div[@class="item-page"]/div[2]/a/@href').extarct()
        for each_download_url in downlaod_urls:

            print each_download_url

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









