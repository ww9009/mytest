import scrapy
import re

from CrawlMacApp.items import CrawlmacappItem

class WwwWmzheComSpider(scrapy.Spider):
    name = "www_wmzhe_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    start_urls = ['http://www.wmzhe.com/fenlei/']

    def parse(self, response):
        all_categories=response.xpath('/html/body/div[4]/div[2]/div/dl/dd/a/@href').extract()
        for each_category in all_categories:
            #print each_category
            try:
                yield scrapy.Request(url=each_category,callback=self.pres_each_category)
            except Exception,e:
                print e.message

    def pres_each_category(self,response):
        try:
            tmp_total_pages=response.xpath('//*[@id="azgame"]/div[2]/div/div[1]/text()').extract()[0]
            pattern = re.compile(r'.?(\d).+')
            total_pages = int(pattern.findall(tmp_total_pages)[0])

            for i in range(1,total_pages+1):
                if i ==1:
                    apply_url=response.url
                else:
                    apply_url=response.url+str(i)+".html"

                yield scrapy.Request(url=apply_url,callback=self.pres_each_page)
                #print apply_url

        except Exception,e:
            print e.message
    def pres_each_page(self,response):
        all_download_link=response.xpath('//*[@id="azgame"]/div[2]/ul/li/div/div[2]/div[1]/a/@href').extract()
        for each_doenload_link in all_download_link:
            #print each_doenload_link
            try:
                yield scrapy.Request(url=each_doenload_link,callback=self.get_each_url)
            except Exception,e:
                pass
    def get_each_url(self,response):
        download_url=response.xpath('//*[@id="xiazai"]/div[2]/div[1]/dl[4]/dd[1]/a/@href').extract()
        allow_postfix=('.dmg','.pkg','.zip')
        for each_download_url in download_url:
            if each_download_url.endswith(allow_postfix):
                item = CrawlmacappItem()
                item['soft_id'] = each_download_url
                item['soft_name'] = ""
                item['download_link'] = each_download_url
                item['is_download'] = False
                item['download_time'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = ""
                yield item
