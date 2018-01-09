# -*- coding: utf-8 -*-
import scrapy
import os
from CrawlMacApp.items import CrawlmacappItem
from scrapy_splash import SplashRequest
import datetime
import re
import time
import datetime

class DownloadDocumentfoundationOrgSpider(scrapy.Spider):
    name = "download_documentfoundation_org_spider"
    allowed_domains = ["download.documentfoundation.org"]
    start_urls = ['http://download.documentfoundation.org/libreoffice/']
    base_url = "http://download.documentfoundation.org/libreoffice/"
    pattern = re.compile(r'<td valign="top">&nbsp;</td><td><a href="(.*)">.*</a>')

    def parse(self, response):
        #采用正则表达式进行提取
        pattern = re.compile(r'<td valign="top">&nbsp;</td><td><a href="(.*)">.*</a>')
        process_branches = pattern.findall(response.body)
        for branch in process_branches[-2:]:
            branch_url=self.base_url+branch
            #处理每个stable or testing branch
            yield scrapy.Request(url=branch_url,callback=self.get_each_edition_branch)

    def get_each_edition_branch(self,response_back):
        #获取每个版本的 URL

        #pattern=re.compile(r'<td valign="top">&nbsp;</td><td><a href="(.*)">.*</a>')
        edition_branchs=self.pattern.findall(response_back.body)
        for each_edition_branch in edition_branchs[-2:]:
            each_edition_branch_url=response_back.url+each_edition_branch
            yield scrapy.Request(url=each_edition_branch_url,callback=self.pres_each_platform)

    def pres_each_platform(self,response):
        #pattern = re.compile(r'<td valign="top">&nbsp;</td><td><a href="(.*)">.*</a>')
        platform_results = self.pattern.findall(response.body)
        for each_platform in platform_results[1:4]:
            each_platform_url=response.url+each_platform
            #print each_platform_url
            yield scrapy.Request(url=each_platform_url,callback=self.pres_each_platform_bits)

    def pres_each_platform_bits(self,response):
        #pattern = re.compile(r'<td valign="top">&nbsp;</td><td><a href="(.*)">.*</a>')
        platform_bits_results = self.pattern.findall(response.body)
        for each_platform_bits_results in platform_bits_results[1:]:
            each_platform_bits_result_url= response.url+each_platform_bits_results
            yield scrapy.Request(url=each_platform_bits_result_url,callback=self.pres_each_apply_url)
            #print each_platform_bits_result_url


    def pres_each_apply_url(self,response):
        sp_pattern = re.compile(r'<td valign="top">&nbsp;</td><td><a href=".*">(.*)</a></td><td.*</td>')
        all_applies_urls=sp_pattern.findall(response.body)

        post_fix=(".gz",".dmg")
        for each_apply_url in all_applies_urls:
            if each_apply_url.endswith(post_fix):
                each_apply_download_url=response.url+each_apply_url
                item=CrawlmacappItem()

                item['soft_id'] = (str(datetime.datetime.now())+each_apply_url).split(" ")[1]
                item['soft_name'] = each_apply_url
                item['download_link'] = each_apply_download_url
                item['is_download'] = False
                item['download_time'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = ""
                yield item








