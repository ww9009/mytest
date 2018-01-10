#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests

class WwwGrandmatrixComSpider(scrapy.Spider):
    name="www_grandmatrix_com_spider"
    base_url="http://www.grandmatrix.com"

    def start_requests(self):
        pages=[37,180,16,183,7,6,3,32,217,20,39,1]
        urls=["http://www.grandmatrix.com/mac/action.html","http://www.grandmatrix.com/mac/adventure.html",
              "http://www.grandmatrix.com/mac/cards.html","http://www.grandmatrix.com/mac/hidden.html",
              "http://www.grandmatrix.com/mac/kids.html","http://www.grandmatrix.com/mac/mahjong.html",
              "http://www.grandmatrix.com/mac/marble.html","http://www.grandmatrix.com/mac/match.html",
              "http://www.grandmatrix.com/mac/puzzles.html","http://www.grandmatrix.com/mac/strategy.html",
              "http://www.grandmatrix.com/mac/time.html","http://www.grandmatrix.com/mac/words.html"]
        for i in range(0,len(pages)):
            yield scrapy.Request(url=urls[i],callback=self.parse,meta={"page":pages[i]})

    def parse(self, response):
        this_pages=response.meta["page"]
        for i in range(1,this_pages+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_url=response.url.split('.html')[0]
                pres_url=tmp_url+"-"+str(i)+".html"

            #print(pres_url)
            yield scrapy.Request(url=pres_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        page_download_urls=response.xpath('//*[@id="mainbox"]/div[@class="lists"]/ul/li/ul/li[1]/a/@href').extract()
        for each_download_link in page_download_urls:
            each_download_url=self.base_url+each_download_link

            re_download_url = requests.head(each_download_url, allow_redirects=True)

            items = CrawlmacappItem()
            items['soft_id'] = re_download_url.url
            items['soft_name'] = ''
            items['download_link'] = re_download_url.url
            items['is_download'] = False
            items['download_time'] = ""
            items['is_upload_ftp'] = False
            items['upload_time'] = ""
            items['upload_file_name'] = ""
            items['download_http_error'] = False
            items['soft_desc'] = ""
            yield items

