import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os

class WwwonlineComSpider(scrapy.Spider):

    name = "test_pconline_com_spider"


    def start_requests(self):
        url_file="/home/smallchild/sample_crawler_master_ww/CrawlMacApp/ww_9009.txt"
        t_f=open(url_file,'r')
        for line_url in t_f.readlines():
            line_url=line_url.split("\n")[0]
            #print line_url

            yield SplashRequest(url=line_url,callback=self.get_each_download_link)

    def get_each_download_link(self,response):
        pattern=re.compile(r'.*\'(.*)\'')
        onclick_content=response.xpath('//*[@id="JsoftDes"]/div[1]/a[4]/@onclick').extract()[0]
        onclick_content_element=pattern.findall(onclick_content)[0]
        tmp_download_url=response.url.split('.html')[0]
        download_url=tmp_download_url+onclick_content_element
        get_platform=response.xpath('//*[@id="Jwrap"]/div[2]/div[2]/div/div[1]/div/div[1]/ul/li[6]/text()').extract()[0]
        allow_platform='Mac'

        if get_platform==allow_platform:
            try:

                yield SplashRequest(url=download_url,callback=self.get_each_download_url)
            except Exception,e:
                pass

    def get_each_download_url(self,response):
        real_doanload_url=response.xpath('//*[@id="1"]/div[1]/p[2]/span[2]/a[1]/@href').extract()[0]
        allow_postfix = ('.dmg', '.zip', '.tar', '.pkg')
        if real_doanload_url.endswith(allow_postfix):
            item = CrawlmacappItem()
            item['soft_id'] = real_doanload_url
            item['soft_name'] = ""
            item['download_link'] = real_doanload_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item

