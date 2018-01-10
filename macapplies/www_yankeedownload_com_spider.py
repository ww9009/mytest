#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwYankeedownloadComSpider(scrapy.Spider):
    name="www_yankeedownload_com_spider"
    start_urls=["http://www.yankeedownload.com/download-categories.php"]

    base_url="http://www.yankeedownload.com"
    pattern=re.compile(r's=(.*)')
    pattern_2 = re.compile(r'.*?(\d+)')

    def parse(self, response):
        categories=response.xpath('//*[@id="middlepanel"]/div/div/div/div[2]/div/a/@href').extract()
        for each_category in categories:
            each_category_url=self.base_url+each_category
            try:
                time.sleep(0.1)
                yield scrapy.Request(url=each_category_url,callback=self.parsea_each_category)
            except Exception,e:
                pass

    def parsea_each_category(self,response):
        tmp_category_items=response.xpath('//*[@id="middlepanel"]/div/div[2]/div/span[1]/text()').extract()[0]
        category_items=self.pattern_2.findall(tmp_category_items)
        total_items= category_items[0]
        total_pages=int(total_items)/10+1
        print response.url
        print total_pages







'''
    def start_requests(self):
        for i in range(1,661):
            if i==1:
                pres_url="http://www.yankeedownload.com/search-software-download.php?s=Mac"

            else:
                pres_url="http://www.yankeedownload.com/search-software-download.php?page="+str((i-1)*10)+"&s=mac"
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):
        page_download_links=response.xpath('//body//div[@class="tabletitle_catsoft"]//div[2]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            #print(each_download_url)
            #time.sleep(0.2)
            yield SplashRequest(url=each_download_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):
        print response.url
        print response.body

        download_links=response.xpath('//body//center/a[1]/@href').extract()

        #print download_links
        for each_download_link in download_links:
            #print(each_download_link)
            re_download_url=self.pattern.findall(each_download_link)
            re_download_url=re_download_url[0]

            #print re_download_url

            # items = CrawlmacappItem()
            # items['soft_id'] = re_download_url
            # items['soft_name'] = ''
            # items['download_link'] = re_download_url
            # items['is_download'] = False
            # items['download_time'] = ""
            # items['is_upload_ftp'] = False
            # items['upload_time'] = ""
            # items['upload_file_name'] = ""
            # items['download_http_error'] = False
            # items['soft_desc'] = ""
            #
            # yield items
'''
