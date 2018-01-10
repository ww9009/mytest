import scrapy
import re
from scrapy_splash import SplashRequest

from CrawlMacApp.items import CrawlmacappItem

class Www9thComSpider(scrapy.Spider):
    name = "www_9th_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ['http://s.9ht.com/cse/search?q=mac&p=9&s=10517699197560052058&srt=def&nsid=0&entry=1&area=1']


    def  start_requests(self):
        for i in range(0,141):
            tar_url="http://s.9ht.com/cse/search?q=mac&p="+str(i)+"&s=10517699197560052058&srt=def&nsid=0&entry=1&area=1"
            try:
                yield scrapy.Request(url=tar_url,callback=self.parse)
            except Exception,e:
                pass

    def parse(self, response):
        all_download_links=response.xpath('//*[@id="results"]/div[2]/div/div/h3/a/@href').extract()
        for each_download_link in all_download_links:
            try:
                #print each_download_link
                yield SplashRequest(url=each_download_link,callback=self.get_each_download_url)
            except Exception,e:
                pass

    def get_each_download_url(self,response):
        download_url=response.xpath('//*[@id="addressWrap"]/div[2]/div[1]/ul/li[1]/a/@href').extract()
        for each_download_url in download_url:
            allow_postfix = ('.dmg', '.zip', '.tar', '.pkg')
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


