#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwZolComSpider(scrapy.Spider):
    name="www_zol_com_spider"
    #start_urls=["http://xiazai.zol.com.cn/mac.html"]
    tar_url="http://xiazai.zol.com.cn/mac.html"
    def start_requests(self):
        for i in range(1,30):
            if i==1:
                pres_url=self.tar_url
            else:
                tmp_url=self.tar_url.split('.html')[0]
                pres_url=tmp_url+"_"+str(i)+".html"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)
    def pres_each_page(self,response):
        page_download_urls=response.xpath('//*[@id="cateInfo"]/div[2]/div[1]/ul/li/a/@href').extract()
        for each_download_link in page_download_urls:
            yield SplashRequest(url=each_download_link,callback=self.get_each_download_url)

    def get_each_download_url(self,response):
        download_urls=response.xpath('//*[@id="detail_package"]/@href').extract()
        for each_download_url in download_urls:

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

