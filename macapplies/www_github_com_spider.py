# -*- coding: utf-8 -*-

import scrapy
import os
import time
from CrawlMacApp.items import CrawlmacappItem
import lxml
from lxml import etree
import urllib2
import urllib

# class WwwGithubComSpider(scrapy.Spider):
#
#     name = "www_github_com"
#     allow_domains=["www.github.com"]
#     start_urls=["https://github.com/FreeCAD/FreeCAD/releases/"]
#     base_url="https://github.com"
#
#     def parse(self, response):
#         print response.url
#         print response.body
#
#
#         #all_download_uerls=response.xpath('//div[contains(@class,"release label)]//ul[contains(@class,"release-downloads")]/li/a/@href').extract()
#         all_download_uerls=response.xpath('//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[2]/div[1]/div[2]/ul/li[3]/a/@href').extract()
#
#         for each_download_link in all_download_uerls:
#             print each_download_link

# sou_url="https://github.com/FreeCAD/FreeCAD/releases/"
# header={"User-Agent":"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"}
#
# request=urllib2.Request(url=sou_url,headers=header)
# response=urllib2.urlopen(request).read()
# content=etree.HTML(response)
#
# results=content.xpath('//div[contains(@class,"release label)]//ul[contains(@class,"release-downloads")]/li/a/@href')
#
# print type(results)

