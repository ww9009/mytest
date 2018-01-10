#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwDownloadstockComSpider(scrapy.Spider):
    name = "www_downloadstock_com_spider"
    start_urls=["http://www.downloadstock.biz/"]
    base_url="http://www.downloadstock.biz"


    def start_requests(self):
        urls=[
        "http://www.downloadstock.biz/Audio-Multimedia/","http://www.downloadstock.biz/Business/",
        "http://www.downloadstock.biz/Communications/","http://www.downloadstock.biz/Desktop/",
        "http://www.downloadstock.biz/Development/","http://www.downloadstock.biz/Education/",
        "http://www.downloadstock.biz/Games-Entertainment/","http://www.downloadstock.biz/Graphic-Apps/",
        "http://www.downloadstock.biz/Home-Hobby/","http://www.downloadstock.biz/Network-Internet/",
        "http://www.downloadstock.biz/Security-Privacy/","http://www.downloadstock.biz/Servers/",
        "http://www.downloadstock.biz/System-Utilities/","http://www.downloadstock.biz/Web-Development/"
        ]
        for each_url in urls:
            yield scrapy.Request(url=each_url,callback=self.parse)

    def parse(self, response):
        pattern = re.compile(r'(\d+)')
        tmp_category_items=response.xpath('//*[@id="cont_right"]/div[2]/text()').extract()[0]
        category_items=pattern.findall(tmp_category_items)
        total_pages=int(category_items[0])/12+1

        for i in range(1,total_pages+1):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+str(i-1)+"/latest.html"
            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)
    def parse_each_page(self,response):
        page_download_links=response.xpath('//*[@id="cont_right"]/div/div[1]/a[1]/@href').extract()
        for each_downlaod_link in page_download_links[1:-1]:
            each_downlaod_url=self.base_url+each_downlaod_link
            #print each_downlaod_url
            yield scrapy.Request(url=each_downlaod_url,callback=self.parse_each_downlaod_link)

    def parse_each_downlaod_link(self,response):
        this_platform_info=response.xpath('//*[@id="cont_right"]/div[@class="backgound_1"]/a/text()').extract()
        plat_s=""
        for elem in this_platform_info:
            plat_s+=elem
        if "Mac" in plat_s:
            download_links=response.xpath('//*[@id="cont_right"]/div[4]/a/@href').extract()
            for each_download_link in download_links:
                yield scrapy.Request(url=each_download_link,callback=self.get_each_download_url)


    def get_each_download_url(self,response):
        print response.url
        download_urls=response.xpath('//body//div[@style="float:left; width:350px"]/div/a[1]/@href').extract()
        for each_download_url in download_urls:
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












