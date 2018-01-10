#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwCcmComSpider(scrapy.Spider):
    name="www_ccm_com_spider"

    base_url="http://ccm.net"

    def start_requests(self):
        for i in range(1,24):
            if i==1:
                pres_url="http://ccm.net/download/mac/"
            else:
                pres_url="http://ccm.net/download/mac/?page="+str(i)
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):

        page_links=response.xpath('//*[@id="download_ctn"]/section[2]/ul/li/div[1]/h2/a/@href').extract()
        for each_link in page_links:
            each_url=self.base_url+each_link
            #print each_url
            yield scrapy.Request(url=each_url,callback=self.get_each_download_url)
    def get_each_download_url(self,response):
        download_urls=response.xpath('//*[@id="dlButton"]/@data-url').extract()
        for each_download_url in download_urls[1:]:

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




