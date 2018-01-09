# -*- coding: utf-8 -*-
import os
import re
import scrapy
import sys
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
import time
from CrawlMacApp.items import CrawlmacappItem
import csv
import urllib2
from lxml import etree

class SampleGithub(scrapy.Spider):
    name = 'sample_github_spider'
    sou_path = os.getcwd()
    base_url = "https://github.com"
    # allowed_domains = ['python.org']
    # start_urls = ['http://www.sina.com.cn/']
    #sav_file = open("github_duzixi.txt", 'a+')


    def start_requests(self):
        d_f = '/home/smallchild/sample_crawler_master_ww/CrawlMacApp/spiders/mytest.csv'
        os.chdir('/home/smallchild/sample_crawler_master_ww/gazers_repos')
        reader = csv.reader(open(d_f, 'rU'), dialect='excel')
        for each in reader:
            each_gazer = each[0]
            each_gazer_repositories=each_gazer+"?tab=repositories"
            #print each_gazer_repositories
            yield scrapy.Request(url=each_gazer_repositories, callback=self.parse)


    def parse(self, response):
        res=response.xpath('//*[@id="user-repositories-list"]/ul/li/div[1]/h3/a/@href').extract()

        for each_repo_file in res:
            each_repo_file_url=self.base_url+each_repo_file
            yield scrapy.Request(url=each_repo_file_url,callback=self.pre_each_repo)
    #处理每个仓中的文件
    def pre_each_repo(self,response):
        #print(response.url)
        #获取第一层文件目录
        firstlay_files = response.xpath('//tbody/tr[contains(@class,"js-navigation-item")]/td[contains(@class,"content")]/span/a/@href').extract()
        #sav_file=response.meta["sav_file"]
        for each_firstlay_file in firstlay_files:
            each_firstlay_file_url=self.base_url+each_firstlay_file
            #print(each_firstlay_file_url)

            yield scrapy.Request(url=each_firstlay_file_url,callback=self.pre_fromsecondlay_file)

    def pre_fromsecondlay_file(self,response):
        pro_url=response.url
        print(pro_url)
        sav_gazer=pro_url.split('/')[3]
        sav_file="github.com_"+sav_gazer+".txt"

        #print(sav_file)

        try:
            t_f=open(sav_file,'a+')
            secondlay_files=response.xpath('//tr[@class="js-navigation-item"]/td[2]/span/a/@href').extract()
            if len(secondlay_files)>0:
                for each in secondlay_files:
                    each_url=self.base_url+each
                    yield scrapy.Request(url=each_url,callback=self.pre_fromsecondlay_file)
            if len(secondlay_files)==0:
                #写入本地文件
                t_f.write(response.url+'\n')
            #os.chdir(self.sou_path)
        except Exception,e:
            print(e.message)


