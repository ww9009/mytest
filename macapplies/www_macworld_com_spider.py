#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwMacworldComSpider(scrapy.Spider):
    name="www_macworld_com_spider"

    #start_urls=["https://www.macworld.co.uk/download/mac/"]

    def start_requests(self):

        # category_urls=["https://www.macworld.co.uk/download/mac/audio-video-photo/","https://www.macworld.co.uk/download/mac/backup-recovery/",
        #                 "https://www.macworld.co.uk/download/mac/design-illustration/","https://www.macworld.co.uk/download/mac/developer-programming/",
        #                "https://www.macworld.co.uk/download/mac/disc-burning/","https://www.macworld.co.uk/download/mac/finance-accounts/",
        #                "https://www.macworld.co.uk/download/mac/games/","https://www.macworld.co.uk/download/mac/hobbies-home-entertainment/",
        #                "https://www.macworld.co.uk/download/mac/internet-tools/","https://www.macworld.co.uk/download/mac/kids-education/",
        #                "https://www.macworld.co.uk/download/mac/networking-tools/","https://www.macworld.co.uk/download/mac/office-business/",
        #                "https://www.macworld.co.uk/download/mac/operating-systems-distros/","https://www.macworld.co.uk/download/mac/portable-applications/",
        #                "https://www.macworld.co.uk/download/mac/security/","https://www.macworld.co.uk/download/mac/social-networking/",
        #                "https://www.macworld.co.uk/download/mac/system-desktop-tools/"
        #                ]
        category_urls =["https://www.macworld.co.uk/download/mac/audio-video-photo/"]
        for each_category_url in category_urls:
            #print each_category_url
            yield SplashRequest(url=each_category_url,callback=self.parse)



    def parse(self, response):
        #x1="//*[@id="mainContent"]/h3[1]"
        #x2=//*[@id="filterCatMenu"]/ul/li[1]/a/@href
        print(response.url)
        print response.body


        download_urls=response.xpath('//*[@id="mainContent"]/div[1]/article/div/a/@href').extract()
        for eact_download_link in download_urls:
            print(eact_download_link)