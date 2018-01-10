import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem
import time
import re
import os

class WwwPconlineComSpider(scrapy.Spider):

    name = "www_pconline_com_spider"
    start_urls=["http://dl.pconline.com.cn/fenlei.html"]

    def parse(self, response):
        all_categories=response.xpath('//div[@class="bd col-init"]/div[@class="col-l"]/div[@class="bd"]/dl/dd/a/@href').extract()
        for each_category_url in all_categories:
            each_category_url_1=each_category_url.split(".html")[0]
            each_category_url_2=each_category_url_1+"-1.html"
            #print each_category_url_2
            try:
                yield scrapy.Request(url=each_category_url_2,callback=self.pres_each_category)
                #time.sleep(0.1)
            except Exception,e:
                pass

    def pres_each_category(self,response):
        tmp_total_page=response.xpath('//*[@id="Jwrap"]/div[@class="area sc-1"]//div[@class="box"]/div[@class="bd"]//div[@class="page"]/a/text()').extract()
        if len(tmp_total_page)>0:
            total_page=int(tmp_total_page[-1])
            if total_page>30:
                total_page=30
                for i in range(1,total_page+1):
                    if i==1:
                        each_page_url=response.url
                    else:
                        tmp_each_page_url=response.url.split('.html')[0]
                        each_page_url=tmp_each_page_url+"-"+str(i)+".html"
                    yield scrapy.Request(url=each_page_url,callback=self.get_page_all_download_links)

    def get_page_all_download_links(self,response):
        all_download_urls=response.xpath('//*[@id="Jwrap"]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/p/a/@href').extract()
        #get local download links file

        # t_f=open("ww_9009.txt",'a+')

        for each_download_link in all_download_urls:
            try:
                # print each_download_link
                # t_f.write(each_download_link+'\n')

                yield SplashRequest(url=each_download_link,callback=self.get_each_download_link)
            except Exception,e:
                pass

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
                print download_url

                #yield SplashRequest(url=download_url,callback=self.get_each_download_url)
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

