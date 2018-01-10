#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os
import urllib2


class WwwBkillComSpider(scrapy.Spider):
    name = "www_bkill_com_spider"
    base_url="http://www.bkill.com/download/"
    start_urls=["http://www.bkill.com/download/"]
    #获取所有分类标签
    def parse(self, response):
        all_category=response.xpath('/html/body/div[4]/div[3]/dl/dd/div/a/@href').extract()
        for each_category in all_category:
            each_category=self.base_url+each_category
            try:
                yield scrapy.Request(url=each_category,callback=self.pres_each_category)
            except IndexError:
                pass

    #处理每一类别
    def pres_each_category(self,response):
        #print response.url

        #获取每一类别的 page 数
        total_page=response.xpath('//body/div[4]/div[3]/div[1]/div[2]/div/div/span[2]').extract()[0]
        pattern=re.compile(r'.*?(\d+).*')
        pages=pattern.findall(total_page)[0]
        for i in range(1,int(pages)+1):
            if i==1:
                page_url=response.url
            else:
                tmp_1=a=response.url.split('/')[-1].split('.')[0]
                this_pattern = re.compile(r'(.*)-.*')
                tmp_2 = this_pattern.findall(tmp_1)[0]
                page_url=self.base_url+tmp_2+"-"+str(i)+".html"
            #print page_url
            yield scrapy.Request(url=page_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        page_download_links=response.xpath('//body/div[4]/div[3]/div[1]/div[2]/div/ul/li/div[3]/div[1]/a/@href').extract()
        for each_download_link in page_download_links:
            each_download_link=self.base_url+each_download_link
            #print each_download_link

            yield SplashRequest(url=each_download_link,callback=self.pres_each_download_link)

    def pres_each_download_link(self,response):
        print response.url

        allow_platform_key_words = ('Mac', 'MAC')
        this_platform_imfo = response.xpath('//body/div[@class="wrap"]//ul[@class="soft-param-info-hd clearfix"]/li[4]').extract()[0]
        download_url = response.xpath('//*[@id="soft-downUrl"]/div[3]/div[1]/div[1]/div[2]/ul/li[1]/a/@href').extract()[0]
        item = CrawlmacappItem()
        item['soft_id'] = download_url
        item['soft_name'] = this_platform_imfo
        item['download_link'] = download_url
        item['is_download'] = False
        item['download_time'] = ""
        item['is_upload_ftp'] = False
        item['upload_time'] = ""
        item['upload_file_name'] = ""
        item['download_http_error'] = False
        item['soft_desc'] = ""
        yield item

        # for platform_key_word in allow_platform_key_words:
        #     if platform_key_word in this_platform_imfo:
        #         download_url=response.xpath('//*[@id="soft-downUrl"]/div[3]/div[1]/div[1]/div[2]/ul/li[1]/a/@href').extract()[0]
        #         print download_url
        #
        #         item = CrawlmacappItem()
        #         item['soft_id'] = download_url
        #         item['soft_name'] = ""
        #         item['download_link'] = download_url
        #         item['is_download'] = False
        #         item['download_time'] = ""
        #         item['is_upload_ftp'] = False
        #         item['upload_time'] = ""
        #         item['upload_file_name'] = ""
        #         item['download_http_error'] = False
        #         item['soft_desc'] = ""
        #         yield item








