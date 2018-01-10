#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwWindows9ComSpider(scrapy.Spider):
    name="www_windows9download_com_spider"
    base_url="http://mac.windows9download.net"
    def start_requests(self):

        for i in range(1,21):
            if i==1:
                pres_url="http://mac.windows9download.net/"
            else:
                pres_url="http://mac.windows9download.net/index_"+str(i)+".html"
            yield scrapy.Request(url=pres_url,callback=self.parse)

    def parse(self, response):

        page_download_links=response.xpath('//*[@id="content"]/div/table/tbody/tr/td/div[2]/div/a/@href').extract()
        for each_downlaod_link in page_download_links:
            each_downlaod_url=self.base_url+each_downlaod_link

            yield scrapy.Request(url=each_downlaod_url,callback=self.parse_each_downlaod_link)
    def parse_each_downlaod_link(self,response):
        downlaod_links=response.xpath('//body//table/tbody/tr[2]/td[@width="350"]/a/@href').extract()

        pattern=re.compile(r'<a href="(.*)".*target="_blank"><img')
        ans=pattern.findall(response.body)


        for each_download_link in ans:

            each_download_url=self.base_url+each_download_link
            print each_download_url

            yield scrapy.Request(url=each_download_url,callback=self.get_each_downlaod_url)
    def get_each_downlaod_url(self,response):
        #print response.url

        download_urls=response.xpath('//*[@id="categories-5"]/div[3]/ul/a/@href').extract()
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
