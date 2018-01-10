#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwWinsiteComSpider(scrapy.Spider):

    name = "www_winsite_com_spider"
    start_urls=["http://www.winsite.com/browse/"]

    def parse(self, response):
        categories=response.xpath('//*[@id="main"]/div/div[4]/div/ul/li/a[1]/@href').extract()
        for each_category_url in categories:
            yield SplashRequest(url=each_category_url,callback=self.pres_each_category)

    def pres_each_category(self,response):
        tmp_category_pages=response.xpath('//body//div[@id="main"]/div[@style="float: left;"]/a/text()').extract()
        category_pages=int(tmp_category_pages[-2])
        for i in range(1,category_pages+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+str(i)+"/"
            try:
                yield scrapy.Request(url=pres_url,callback=self.pres_each_page)
            except Exception,e:
                pass

    def pres_each_page(self,response):
        print response.url

        this_page_platform=response.xpath('//body//div[@class="cat"]/ul/li//ul[@class="third-list"]/li/span/text()').extract()
        this_page_download_urls=response.xpath('//body//div[@class="cat"]/ul/li//div[@class="btn"]/a[@class="download"]/@href').extract()

        #print len(this_page_platform)
        #print len(this_page_download_urls)

        for each_platform in this_page_platform:
             plat_info=each_platform.split(' ')
             if "Mac" in plat_info:
                 # get the posi_id of available url
                 posi_id=this_page_platform.index(each_platform)

                 download_url= this_page_download_urls[posi_id]
                # redirect the download_url
                 #re_download_url=requests.head(download_url,allow_redirects=True)

                 item = CrawlmacappItem()
                 item['soft_id'] = download_url
                 item['soft_name'] = ""
                 item['download_link'] = download_url
                 item['is_download'] = False
                 item['download_time'] = ""
                 item['is_upload_ftp'] = False
                 item['upload_time'] = ""
                 item['upload_file_name'] = ""
                 item['download_http_error'] = False
                 item['soft_desc'] = ""
                 yield item







