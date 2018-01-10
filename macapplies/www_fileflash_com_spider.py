#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwFileflashComSpider(scrapy.Spider):
    name = "www_fileflash_com_spider"
    start_urls=["http://www.fileflash.com/"]

    def start_requests(self):
        urls=[
            "http://www.fileflash.com/software/category/1/","http://www.fileflash.com/software/category/132/",
            "http://www.fileflash.com/software/category/2/","http://www.fileflash.com/software/category/69/",
            "http://www.fileflash.com/software/category/14/","http://www.fileflash.com/software/category/201/",
            "http://www.fileflash.com/software/category/24/","http://www.fileflash.com/software/category/204/",
            "http://www.fileflash.com/software/category/23/","http://www.fileflash.com/software/category/245/",
            "http://www.fileflash.com/software/category/43/"
            ]

        pages=[188,237,31,198,1,68,278,141,210,39,231]
        for i in range(len(urls)):
            yield scrapy.Request(url=urls[i],callback=self.parse,meta={"pages":pages[i]})


    def parse(self, response):

        category_pages=response.meta["pages"]
        #print(response.url)
        #print(category_pages)

        for i in range(1,int(category_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+"page"+str(i)+".html"
            yield SplashRequest(url=pres_url,callback=self.parse_each_page)



    def parse_each_page(self,response):
        page_download_urls = response.xpath(
            '//body//tbody//table[@class="description"]//td[@class="download"]//tbody/tr/td[2]/a/@href').extract()
        thispage_platform_inform = response.xpath(
            '//body//tbody//table[@class="description"]//tbody//tbody/tr/td[3]/text()').extract()




        for each_download_url in page_download_urls:
            try:
                yield SplashRequest(url=each_download_url,callback=self.parse_each_download_link)
            except Exception,e:
                pass

    def parse_each_download_link(self,response):

        download_link1 = response.xpath('//body//tbody/tr[2]/td/strong/a/@href').extract()
        allow_postfix=('.dmg','.zip','.pkg','.tz')
        for each_downlod_url in download_link1:
            re_download_url = requests.head(each_downlod_url, allow_redirects=True)

            if re_download_url.url.endswith(allow_postfix):

                item=CrawlmacappItem()
                item['soft_id'] = re_download_url.url
                item['soft_name'] = ''
                item['download_link'] = re_download_url.url
                item['is_download'] = False
                item['download_time'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = ""

                yield item




'''
    def parse_each_category(self,response):

        print(response.url)

        #category_pages=response.xpath('//body//tbody/tr[2]/td/table/tbody/tr/td[1]/a/text()').extract()[-2]
        #for i in range(1,int(category_pages)+1):
        #    if i==1:
        #        pres_url=response.url
        #    else:
        #        pres_url=response.url+"page"+str(i)+".html"
        #    yield scrapy.Request(url=pres_url,callback=self.parse_each_page)

    def parse_each_page(self,resposne):
        page_download_urls=resposne.xpath('//body//tbody//table[@class="description"]//td[@class="download"]//tbody/tr/td[2]/a/@href').extarct()

        thispage_platform_inform=resposne.xpath('//body//tbody//table[@class="description"]//tbody//td[3]/text()').extract()
        # judge is Mac in this_platform_inform

        

        for each_downlaod_url in page_download_urls:
            #print each_downlaod_url
            yield scrapy.Request(url=each_downlaod_url,callback=self.parse_each_downlaod_url)

    def parse_each_downlaod_url(self,response):
        download_link1=response.xpath('//body//tbody/tr[2]/td/strong/a/@href').extarct()
        for each_downlod_url in download_link1:

            pass
'''


