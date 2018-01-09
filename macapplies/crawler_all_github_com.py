# -*- coding: utf-8 -*-
import scrapy
from CrawlMacApp.items import CrawlmacappItem
import time

class CrawAllGithub(scrapy.Spider):
    name = "crawler_all_github"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ['https://github.com/tensorflow/tensorflow/stargazers/']
    #base_ur= 'https://github.com/tensorflow/tensorflow/stargazers?page='

    def get_eachfirstlayer_gazer(self):
        f = "firstlayer_gazers.txt"
        t_f = open(f, 'r')
        for each_userurl in t_f.readlines():
            each_userurl = each_userurl.split("\n")[0]
            # print each_userurl
            yield scrapy.Request(each_userurl,callback=self.parse)
    def parse(self, response):
        print response.url







