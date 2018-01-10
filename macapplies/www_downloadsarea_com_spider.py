#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwDownloadsareaComSpider(scrapy.Spider):
    name = "www_downloadsarea_com_spider"
    base_url="http://www.downloadsarea.com"

    def start_requests(self):
        for i in range(1,11):
            if i==1:
                pres_url="http://www.downloadsarea.com/Mac/"
            else:
                pres_url="http://www.downloadsarea.com/Mac/"+str(i)+"/"

            yield scrapy.Request(url=pres_url,callback=self.parse)
    def parse(self, response):
        page_download_links=response.xpath('//body//div[@class="ci-item"]/div[@class="cii-fl"]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link

            #print each_download_url
            yield scrapy.Request(url=each_download_url,callback=self.parse_each_downloalink)
    def parse_each_downloalink(self,response):
        download_links=response.xpath('//*[@id="itd-left-dlink"]/ul/li/a/@href').extract()
        for each_download_link in download_links:
            each_download_url=self.base_url+each_download_link

            #re_download_url = requests.head(each_download_url, allow_redirects=True)
            #print re_download_url.url

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



