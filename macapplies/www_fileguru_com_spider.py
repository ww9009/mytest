#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwFileguruComSpider(scrapy.Spider):
    name="www_fileguru_com_spider"
    base_url="http://www.fileguru.com"
    start_urls=["http://www.fileguru.com/directory"]

    def start_requests(self):
        urls=[
                "/directory/Business","/directory/Desktop","/directory/Development",
                "/directory/Education","/directory/Games","/directory/Home---Personal",
                "/directory/Internet","/directory/Mobile","/directory/Multimedia",
                "/directory/Security---Privacy","/directory/Utilities","/directory/Web-Development"
        ]
        pages=[209,16,14,4,245,235,261,1,463,141,751,57]
        for i in range(len(urls)):
            pres_url=self.base_url+urls[i]

            yield scrapy.Request(url=pres_url,callback=self.parse,meta={"pages":pages[i]})

    def parse(self, response):
        pages=response.meta["pages"]

        for i in range(1,int(pages)+1):
             if i==1:
                 pres_url=response.url
             else:
                 pres_url=response.url+"/p"+str(i)

             yield scrapy.Request(url=pres_url,callback=self.parse_each_page)

    def parse_each_page(self,response):

        page_download_links=response.xpath('//body//div/nobr/ul/li[1]/a/@href').extract()
        page_platform_info=response.xpath('//body//div[@class="product_row"]/p[3]/span').extract()
        for i in range(len(page_platform_info)):
            if "Mac" in page_platform_info[i]:
                pres_url=self.base_url+page_download_links[i]
                yield scrapy.Request(url=pres_url,callback=self.parse_each_download_link)

    def parse_each_download_link(self,response):

        download_links=response.xpath('//*[@id="noborder"]/span/a/@href').extract()
        for each_download_link in download_links:
            each_download_url=self.base_url+each_download_link

            #re_download_url=requests.head(each_download_url,allow_redirects="True")
            items = CrawlmacappItem()
            items['soft_id'] = each_download_url
            items['soft_name'] = ''
            items['download_link'] = each_download_url
            items['is_download'] = False
            items['download_time'] = ""
            items['is_upload_ftp'] = False
            items['upload_time'] = ""
            items['upload_file_name'] = ""
            items['download_http_error'] = False
            items['soft_desc'] = ""
            yield items











