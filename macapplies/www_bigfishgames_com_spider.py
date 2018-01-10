import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2
import requests

class WwwBigfishgameComSpider(scrapy.Spider):
    name = "www_bigfishgame_com_spider"
    start_urls=["https://www.bigfishgames.com/mac-games/"]

    def parse(self, response):
        categories=response.xpath('//*[@id="topgenres"]/ul/li/a/@href').extract()
        for each_category in categories:
            #print each_category
            yield scrapy.Request(url=each_category,callback=self.pres_each_category)

    def pres_each_category(self,response):
        download_urls=response.xpath('//*[@id="genre_bottom_1"]/li/a/@href').extract()
        for each_downlaod_url in download_urls:
            #print each_downlaod_url
            #s="http://downloads.bigfishgames.com/grim-facade-hidden-sins-collectors-edition_s1_l1"
            yield SplashRequest(url=each_downlaod_url,callback=self.get_each_downlaod_url)
    def get_each_downlaod_url(self,response):
        download_urls=response.xpath('//body/div[3]/div/div[3]/div/div[1]/div[2]/div[1]/a/@href').extract()
        for each_download_url in download_urls:

            print each_download_url


