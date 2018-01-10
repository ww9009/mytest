#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class Www3322ComSpider(scrapy.Spider):

    name = "www_3322_com_spider"
    base_url="http://www.3322.cc"

    def start_requests(self):
        for i in range(1,40):
            pres_url="http://www.3322.cc/search.asp?wd=Mac&otype=&lm=1&page="+str(i)
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//body/div[5]/div[1]/div[2]/div/ul/li/div[1]/a/@href').extract()
        for each_download_link in page_download_links:
            yield SplashRequest(url=each_download_link,callback=self.get_each_download_url)
    def get_each_download_url(self,response):

        download_urls=response.xpath('//*[@id="xzdz"]/div[2]/div/div[1]/div/ul[2]/li/a/@href').extract()
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


