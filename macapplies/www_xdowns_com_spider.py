#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwXdownsComSpider(scrapy.Spider):
    name="www_xdowns_com_spider"
    base_url="http://www.xdowns.com"
    base_url2="http://xx153.xdowns.com/soft/"
    #start_urls=["http://mydown.yesky.com/mac"]

    def start_requests(self):
        for i in range(1,291):
            if i==1:
                pres_url="http://www.xdowns.com/soft/184/apple/index.html"
            else:
                pres_url="http://www.xdowns.com/soft/184/apple/Soft_255_"+str(i)+".html"

            yield scrapy.Request(url=pres_url,callback=self.parse)
    def parse(self, response):
        print response.url
        page_download_links=response.xpath('//*[@id="page_content"]/div[3]/div[1]/div/div[2]/ul/li/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            #print each_download_url
            yield scrapy.Request(url=each_download_url,callback=self.pres_each_download_link)

    def pres_each_download_link(self,response):
        download_site_link=response.xpath('//*[@id="cwin"]/@src').extract()[0]
        download_site_url=self.base_url+download_site_link
        #print download_site_url
        try:
            yield SplashRequest(url=download_site_url,callback=self.get_each_download_url)
        except Exception,e:
            pass

    def get_each_download_url(self,response):

        download_urls=response.xpath('//*[@id="download_box"]/div/ul[2]/li[1]/a/@href').extract()
        for each_download_url in download_urls:
            each_download_url=self.base_url2+each_download_url
            #print each_download_url

            item = CrawlmacappItem()
            real_download_url=requests.get(each_download_url,allow_redirects=True)
            item['soft_id'] = real_download_url
            item['soft_name'] = ""
            item['download_link'] = real_download_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item



