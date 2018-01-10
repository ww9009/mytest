#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwSoft32ComSpider(scrapy.Spider):
    name = "www_soft32_com_spider"
    start_urls=["https://www.soft32.com/mac/most-popular/?sort=date_updated_timestamp"]
    #start_urls=["https://www.soft32.com/mac/widgets/5/?s=popularity/"]

    def parse(self, response):
        # content= response.body
        # pattern=re.compile(r'<a href="(.*)" class="soft"')
        # all_download_links=pattern.findall(content)
        # for each_download_link in all_download_links:
        #
        #     print each_download_link

        #all_download_urls=response.xpath('//body//tbody/tr//div/a/@href').extract()
        categories=response.xpath('//*[@id="navigation"]/div[2]/ul[1]/li/a/@href').extract()
        for each_category in categories:
            #print each_category
            yield scrapy.Request(url=each_category,callback=self.pres_each_category)

    def pres_each_category(self,response):
        tmp_total_pages=response.xpath('//body//ul[@class="pagination"]/li/a/span').extract()
        total_pages=tmp_total_pages[-2]
        pattern=re.compile(r'\d+')
        total_pages=int(pattern.findall(total_pages)[0])

        for i in range(1,total_pages+1):
            if i==1:
                pres_url=response.url+"?s=popularity/"
            else:
                pres_url=response.url+str(i)+"/?s=popularity/"

            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):

        content= response.body
        pattern=re.compile(r'<a href="(.*)" class="soft"')
        all_download_links=pattern.findall(content)
        for each_download_link in all_download_links:
            each_download_url=each_download_link+"/free-download/"
            #print each_download_url
            yield scrapy.Request(url=each_download_url,callback=self.get_each_download_url)
    def get_each_download_url(self,response):
        download_urls=response.xpath('//*[@id="download"]/div[1]/div[1]/a/@data-download').extract()
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



