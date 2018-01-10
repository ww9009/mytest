#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwDownloadcollectionComSpider(scrapy.Spider):
    name = "www_downloadcollection_com_spider"
    start_urls=["http://www.downloadcollection.com/category/mac.htm"]
    base_url="http://www.downloadcollection.com"

    def start_requests(self):
        urls=[
        "/category/mac/audio.htm","/category/mac/business.htm",
        "/category/mac/communications.htm","/category/mac/dashboard_widgets.htm",
        "/category/mac/desktop.htm","/category/mac/development.htm",
        "/category/mac/driver.htm","/category/mac/education.htm",
        "/category/mac/games.htm","/category/mac/home___hobby.htm",
        "/category/mac/multimedia___graphics.htm","/category/mac/network___internet.htm",
        "/category/mac/other.htm","/category/mac/screensavers.htm",
        "/category/mac/security.htm","/category/mac/utilities.htm",
        "/category/mac/video.htm"
        ]
        category_pages=[23,118,10,1,23,315,1,158,240,17,152,103,31,3,26,237,47]
        for i in range(len(urls)):
            each_category_url=self.base_url+urls[i]
            yield scrapy.Request(url=each_category_url,callback=self.parse,meta={"pages":category_pages[i]})

    def parse(self, response):
        category_pages=response.meta["pages"]

        # print(response.url)
        # print category_pages
        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:

                tmp_url=response.url.split('.htm')[0]
                pres_url=tmp_url+str(i-1)+".htm"
            try:
                yield SplashRequest(url=pres_url,callback=self.pres_each_page)
            except Exception,e:
                pass

    def pres_each_page(self,response):
        # tf="ww_9009.txt"
        # t_f=open(tf,"a+")

        page_downlaod_links=response.xpath('//*[@id="dl-tbl-list"]/tbody/tr/td[2]/p[1]/a/@href').extract()
        for each_download_link in page_downlaod_links:
            each_download_url=self.base_url+each_download_link

            re_download_url = requests.head(each_download_url, allow_redirects=True)
            #print re_download_url.url

            #print each_download_url
            #t_f.write(each_download_url+"\n")

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


