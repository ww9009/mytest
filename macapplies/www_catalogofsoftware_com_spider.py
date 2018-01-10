#coding=utf-8
import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import re
import os
import requests
import time

class WwwCatalogofsofwareComSpider(scrapy.Spider):
    name = "www_catalogofsoftware_com_spider"
    #start_urls=["http://www.catalogofsoftware.com/?platform=Mac"]


    def start_requests(self):
        urls=[
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Audio%20%26amp%3B%20Multimedia&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Business&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Communications&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Desktop&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Development&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Education&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Games%20%26amp%3B%20Entertainment&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Graphic%20Apps&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Home%20%26amp%3B%20Hobby&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Network%20%26amp%3B%20Internet&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=Security%20%26amp%3B%20Privacy&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Servers&order=Date&filter=Any",
            "http://www.catalogofsoftware.com/index.php?platform=Mac&category=System%20Utilities&order=Date&filter=Any","http://www.catalogofsoftware.com/index.php?platform=Mac&category=Web%20Development&order=Date&filter=Any"

        ]
        for each_url in urls:
            yield SplashRequest(url=each_url,callback=self.parse)

    def parse(self, response):
        category_pages=response.xpath('//body/center/table/tbody/tr[5]/td/p[4]/a/span/text()').extract()

        if len(category_pages)==0:
            total_pages=1
        else:
            total_pages=category_pages[-1]

        for i in range(1,int(total_pages)+1):
            if i==1:
                pres_url=response.url
            else:
                tmp_url=response.url.split('&order')[0]
                pres_url=tmp_url+"&page="+str(i)+"&order=Date&filter=Any&search_type=Keywords"
            yield scrapy.Request(url=pres_url,callback=self.parse_each_page)


            # s="http://www.catalogofsoftware.com/index.php?platform=Mac&category=Development&order=Date&filter=Any"
            # y="http://www.catalogofsoftware.com/index.php?platform=Mac&category=Development&page=2&order=Date&filter=Any&search_type=Keywords"
            #
            # d="http://www.catalogofsoftware.com/index.php?platform=Mac&category=Audio%20%26amp%3B%20Multimedia&order=Date&filter=Any"
            # z="http://www.catalogofsoftware.com/index.php?platform=Mac&category=Audio%20%26amp%3B%20Multimedia&page=3&order=Date&filter=Any&search_type=Keywords"

    def parse_each_page(self,response):
        page_download_urls=response.xpath('//body//td[@class="table_header"]/a/@href').extract()
        for each_downlaod_url in page_download_urls:
            yield SplashRequest(url=each_downlaod_url,callback=self.parse_each_downlaod_url)

    def parse_each_downlaod_url(self,response):
        download_urls=response.xpath('//body//tbody/tr/td[2]/table/tbody/tr/td[@colspan="2"]/a/@href').extract()
        for each_downlaod_url in download_urls:
            yield SplashRequest(url=each_downlaod_url,callback=self.get_each_downloadurl)

    def get_each_downloadurl(self,response):
        download_urls=response.xpath('//body//table/tbody/tr/td[2]/a/@href').extract()
        for each_download_url in download_urls:

            items = CrawlmacappItem()
            items['soft_id'] = each_download_url
            items['soft_name'] = ''
            items['download_link'] = each_download_url
            items['is_download'] = False
            items['download_time'] = ""
            items['is_upload_ftp'] = False
            items['upload_time'] = ""
            items['upload_file_name'] = ""
            items['download_http_error'] = False
            items['soft_desc'] = ""
            yield items







