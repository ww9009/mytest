#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwEurodownloadComSpider(scrapy.Spider):
    name = "www_eurodownload_com_spider"
    base_url="http://www.eurodownload.com"
    pattern = re.compile(r'(http://.*[zip,dmg,pkg,zip,sit,gz])')
    pattern_2=re.compile(r'=(http://.*[zip,dmg,pkg,zip,sit,gz])')

    def start_requests(self):
        for i in range(1,423):
            if i==1:
                pres_url="http://www.eurodownload.com/search-software-downloads.php?s=Mac"
            else:
                pres_url="http://www.eurodownload.com/search-software-downloads.php?o="+str((i-1)*10)+"&s=Mac"
            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)
    def parse_each_page(self,response):
        #print response.url
        page_download_links=response.xpath('//body//div[@class="table_noborder"]//div[@class="ButtonDownload"]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_url=self.base_url+each_download_link
            try:
                yield scrapy.Request(url=each_download_url,callback=self.parse_each_download_link)
            except Exception,e:
                pass

    def parse_each_download_link(self,response):
        download_urls=response.xpath('//*[@id="main"]/div[4]/center/a[1]/@href').extract()
        usgae_url=[]
        for each_downlod_url in download_urls:
            tmp_each_downlod_url=self.pattern.findall(each_downlod_url)
            if len(tmp_each_downlod_url)==0:
                tmp_each_downlod_url=self.pattern_2.findall((each_downlod_url))
                if len(tmp_each_downlod_url)==0:
                    tmp_each_downlod_url=usgae_url.append(each_downlod_url)

            re_download_url=tmp_each_downlod_url[0]

            items = CrawlmacappItem()
            items['soft_id'] = re_download_url
            items['soft_name'] = ''
            items['download_link'] = re_download_url
            items['is_download'] = False
            items['download_time'] = ""
            items['is_upload_ftp'] = False
            items['upload_time'] = ""
            items['upload_file_name'] = ""
            items['download_http_error'] = False
            items['soft_desc'] = ""
            yield items


