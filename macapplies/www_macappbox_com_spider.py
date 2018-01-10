#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwMacappboxComSpider(scrapy.Spider):

    name = "www_macappbox_com_spider"
    start_urls=["http://www.macappbox.com/app/"]
    base_url="http://www.macappbox.com"

    def parse(self, response):
        soft_categories=response.xpath('/html/body/div[1]/dl/dt[@class="dropdown"]/ul/a/@href').extract()

        for each_download_link in soft_categories[:-5]:
            each_download_url=self.base_url+each_download_link

            #print each_download_url
            yield scrapy.Request(url=each_download_url,callback=self.pres_each_category)


    def pres_each_category(self,response):
        #page_download_links=response.xpath('/html/body/div[5]/div[1]/ul/li/a[1]/@href').extract()

        for i in range(1,4):
            if i==1:
                pres_url=response.url
            else:
                tmp_pres_url=response.url
                pres_url=tmp_pres_url+"index_"+str(i)+".html"
            try:

                yield SplashRequest(url=pres_url,callback=self.pres_each_page)
            except Exception,e:
                pass

    def pres_each_page(self,response):
        page_download_links=response.xpath('//body/div[5]/div[1]/ul/li/a[1]/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            try:
                yield SplashRequest(url=each_download_url,callback=self.get_each_download_url)
            except Exception,e:
                pass


    def get_each_download_url(self,response):
        download_urls=response.xpath('//body/div[2]/div/div[1]/span[@class="download"]/a[1]/@href').extract()
        for each_download_link in download_urls:
            each_download_url=self.base_url+each_download_link.split("\n")[1]

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



