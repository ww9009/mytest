#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwXiazaiComSpider(scrapy.Spider):
    name = "www_xiazai_com_spider"

    def start_requests(self):
        pres_urls=["http://www.xiazai.com/ios-72-0-time",
                   "http://www.xiazai.com/ios-84-0-time",
                   "http://www.xiazai.com/ios-97-0-time",
                   "http://www.xiazai.com/ios-152-0-time"]
        total_pages=[30,12,162,36]

        for i in range(0,len(pres_urls)):
            yield scrapy.Request(url=pres_urls[i],callback=self.parse,meta={"pages":total_pages[i]})

    def parse(self, response):

        category_pages=response.meta["pages"]
        for i in range(0,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+"-"+str(i)

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        page_download_urls=response.xpath('//body//div[@class="soft_list"]/dl/dt/a/@href').extract()
        for each_download_url in page_download_urls:
            yield scrapy.Request(url=each_download_url,callback=self.get_each_download_url)
    def get_each_download_url(self,response):
        download_urls=response.xpath('//body//ul[@class="special clearfix"]/li[2]/a/@onclick').extract()
        pattern = re.compile(r'\(\'(.*)\'\)')
        allow_postfix = ('.dmg', '.zip', '.tar', '.pkg', 'rar')

        for each_download_url in download_urls:
            res = pattern.findall(each_download_url)[0]

            re_download_url = requests.head(res, allow_redirects=True)

            #print re_download_url.url

            if re_download_url.url.endswith(allow_postfix):

                item = CrawlmacappItem()
                item['soft_id'] = re_download_url.url
                item['soft_name'] = ""
                item['download_link'] = re_download_url.url
                item['is_download'] = False
                item['download_time'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = ""
                yield item





