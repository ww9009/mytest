# -*- coding: utf-8 -*-
import scrapy
import os
from CrawlMacApp.items import CrawlmacappItem
from scrapy_splash import SplashRequest
import datetime
import re
import time
import datetime

class DownloadCaminbrowserOrgSpider(scrapy.Spider):
    name = "caminbrowser_org_spider"
    #allowed_domains="http://caminobrowser.org/"
    start_urls=["http://caminobrowser.org/download/"]
    base_url="http://caminobrowser.org"

    def parse(self, response):
        all_versions=response.xpath('//*[@id="content"]/ul/li/a/@href').extract()
        for each_version in all_versions[2:]:
            #print(self.base_url+each_version)
            each_version_url=self.base_url+each_version
            yield scrapy.Request(url=each_version_url,callback=self.get_each_download_page,meta={"each_version":each_version})


    def get_each_download_page(self,response):
        each_download_page=response.xpath('//div[@class="col3 rbox clear"]/div/div/p[1]/a/@href').extract()
        each_download_page_url=self.base_url+each_download_page[0]
        #print(each_download_page_url)
        each_version=response.meta["each_version"]
        yield scrapy.Request(url=each_download_page_url,callback=self.get_each_apply_download_url,meta={"each_version":each_version})

    def get_each_apply_download_url(self,response):
        apply_download_urls=response.xpath('//*[@id="content"]/p/a/@href').extract()
        if len(apply_download_urls)==0:
            apply_download_urls=response.xpath('//*[@id="content"]/div[1]/p/a/@href').extract()

        for each_apply_download_url in apply_download_urls:

            download_url=apply_download_urls[0]
            item=CrawlmacappItem()
            soft_name=response.meta["each_version"].strip("/")

            item['soft_id'] = (str(datetime.datetime.now())+soft_name).split(" ")[1]
            item['soft_name'] = soft_name
            item['download_link'] = download_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            # 返回 item 给pipeline
            yield item

