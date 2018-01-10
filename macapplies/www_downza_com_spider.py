#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests



class WwwDownzaComSpider(scrapy.Spider):
    name = "www_downza_com_spider"

    def start_requests(self):
        pres_urls=["http://www.downza.cn/mac/macyx-426-1.html",
                   "http://www.downza.cn/mac/xtrj-301-1.html",
                   "http://www.downza.cn/soft/list302-1.html"]
        total_pages=[75,12,2]

        for i in range(len(pres_urls)):
            yield scrapy.Request(url=pres_urls[i],callback=self.parse,meta={"pages":total_pages[i]})


    def parse(self, response):
        pages=response.meta["pages"]
        # print response.url
        # print pages

        for i in range(1,int(pages)+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_url=response.url.split('.html')[0]
                tmp_url_2=tmp_url.split('-')
                pres_url=tmp_url_2[0]+"-"+tmp_url_2[1]+"-"+str(i)+".html"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)
    def pres_each_page(self,response):
        page_download_urls=response.xpath('//body//div[@class="bd"]/ul/li//div[@class="list-img"]/a/@href').extract()
        for each_download_page_url in page_download_urls:
            yield scrapy.Request(url=each_download_page_url,callback=self.get_each_download_url)

    def get_each_download_url(self,response):
        download_urls=response.xpath('//body//div[@class="down_bottom"]/ul/li/a/@href').extract()
        allow_postfix = ('.dmg', '.zip', '.tar', '.pkg', 'rar')
        #print download_urls
        t_f="tmp001.txt"
        fil=open(t_f,'a+')

        for each_download_url in download_urls:
            re_download_url=requests.head(each_download_url,allow_redirects=True)
            if re_download_url.url.endswith(allow_postfix):
                fil.write(re_download_url.url+"\n")


                # item = CrawlmacappItem()
                # item['soft_id'] = re_download_url.url
                # item['soft_name'] = ""
                # item['download_link'] = re_download_url.url
                # item['is_download'] = False
                # item['download_time'] = ""
                # item['is_upload_ftp'] = False
                # item['upload_time'] = ""
                # item['upload_file_name'] = ""
                # item['download_http_error'] = False
                # item['soft_desc'] = ""
                # yield item

