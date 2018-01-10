#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwMacdownloadComSpider(scrapy.Spider):
    name="www_macdownload_com_spider"

    start_urls=["http://macdownload.informer.com/Ct/Audio-Video/"]

    def parse(self, response):

        categories=response.xpath('//body/header/div[3]//div/nav/ul/li/a/@href').extract()
        for i in range(len(categories)):
            #print categories[i]
            yield scrapy.Request(url=categories[i],callback=self.pres_each_category,meta={"i_d":i})

    def pres_each_category(self,response):
        i_d=response.meta["i_d"]
        catrgory_pages=[400,306,89,306,189,211,400,130,118,217,60,400,102,400]
        #print response.url
        #print catrgory_pages[i_d]
        for i in range(1,catrgory_pages[i_d]+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+"page/"+str(i)+"/"

            #print pres_url
            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)


    def pres_each_page(self,response):
        page_download_urls=response.xpath('//*[@id="content"]/section/div//section//div[1]/a/@href').extract()
        for each_download_page_url in page_download_urls:
            #print each_download_page_url
            yield scrapy.Request(url=each_download_page_url,callback=self.pres_each_download_page)

    def pres_each_download_page(self,response):

        download_link=response.xpath('//body/div/div/article/div/section/div/figure/div/a/@href').extract()[0]
        #print download_link

        each_download_url=download_link+"#downloading"
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


