# -*- coding: utf-8 -*-

import scrapy
import os
import time
from CrawlMacApp.items import CrawlmacappItem

class FosshubComSpider(scrapy.Spider):
    name = 'www_fosshub_com'
    allowed_domains = ['www.fosshub.com']
    start_urls = ['https://www.fosshub.com/']
    base_url="https://www.fosshub.com"

    # def get_each_category(self,response):
    #
    #     pass
    def parse(self, response):
        #print response.body

        categories_1=response.xpath('//div[contains(@class,"top-categories")]//div[contains(@class,"nav nav-pills text-center")]/a/@href').extract()
        categories_2=response.xpath('//div[contains(@class,"top-categories")]//div[contains(@id,"collapse")]/a/@href').extract()
        categories=categories_1+categories_2
        for eachcategory in categories:
            #print self.base_url+eachcategory
            eachcategory=self.base_url+eachcategory
            yield scrapy.Request(url=eachcategory,callback=self.get_eachpage_app_url)

    def get_eachpage_app_url(self,response):

        apps_urls=response.xpath('//div[contains(@class,"category-list")]/div[contains(@class,"category-list-item")]//h3/a/@href').extract()
        page_apps_num =len(apps_urls)
        #print "Thia page have"+str(page_apps_num)+"app"
        #time.sleep(1)
        for each_app_url in apps_urls:
            each_app_url=self.base_url+each_app_url
            yield scrapy.Request(each_app_url,callback=self.press_eachapp_downloadurl)

            #print each_app_url

    def press_eachapp_downloadurl(self,response):
        app_posifix=(".pkg",".7z",".zip",".dmg")
        #由于 fdslwdx 是随机生成的所以具有不定性，不可取，所以选取 href 进行拼接 亦可实现之
        each_app_download_url=response.xpath('//div[@class="software-headline"]//div[@class="download-section main-dl-box"]/p/a/@fdslwdx').extract()


        for each_app_platform_download_url in each_app_download_url:

             if each_app_platform_download_url.endswith(app_posifix):
                print each_app_platform_download_url

                # item = CrawlmacappItem()
                # item['soft_id'] = ""
                # item['soft_name'] = ""
                # item['download_link'] = each_app_platform_download_url
                # item['is_download'] = False
                # item['download_time'] = ""
                # item['is_upload_ftp'] = False
                # item['upload_time'] = ""
                # item['upload_file_name'] = ""
                # item['download_http_error'] = False
                # item['soft_desc'] = ""
                #
                # yield item


