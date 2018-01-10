#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwDownsinaComSpider(scrapy.Spider):

    name = "www_downsina_com_spider"
    base_url="http://down.tech.sina.com.cn"

    def start_requests(self):
        for i in range(1,69):
            pres_url="http://down.tech.sina.com.cn/download/search.php?f_name=Mac&sort=2&cp="+str(i)
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//*[@id="S_Cont_20"]/ul/li/h2/a[1]/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            #print each_download_url
            yield scrapy.Request(url=each_download_url,callback=self.pres_each_doanload_page)

    def pres_each_doanload_page(self,response):
        download_link= response.xpath('//*[@id="cs_m"]/div[2]/div[2]/p[2]/a/@href').extract()
        for each_link in download_link:
            each_url=self.base_url+each_link

            yield SplashRequest(url=each_url,callback=self.get_each_download_url)
    def get_each_download_url(self,response):

        downlooad_urls=response.xpath('//*[@id="cs_m"]/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/a[1]/@href').extract()
        for each_download_url in downlooad_urls:
            if each_download_url.startswith("http:")==0:
                each_redownload_url=self.base_url+each_download_url
            else:
                each_redownload_url=each_download_url

            item = CrawlmacappItem()
            item['soft_id'] = each_redownload_url
            item['soft_name'] = ""
            item['download_link'] = each_redownload_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item





