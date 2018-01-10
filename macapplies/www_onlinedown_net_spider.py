import scrapy

from CrawlMacApp.items import CrawlmacappItem

class WwwOnlineDownNetSpider(scrapy.Spider):
    name = "www_onlinedown_net_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    start_urls = ['http://www.onlinedown.net/sort/mac/']


    def parse(self, response):
        all_categories=response.xpath('//*[@id="classlist"]/li/a/@href').extract()
        for each_category in all_categories:
            each_category_url="http://www.onlinedown.net"+each_category
            yield scrapy.Request(url=each_category_url,callback=self.pres_each_category)

    def pres_each_category(self,response):
        tmp_total_page=response.xpath('/html/body/div[5]/div[2]/div[1]/div[3]/span/text()').extract()[0][1:-1]
        total_page=int(tmp_total_page)+1
        #print response.url

        for i in range(1,total_page):
            if i==1:
                pres_url=response.url
            else:
                pres_url=response.url+str(i)+"/"

            #print pres_url
            yield scrapy.Request(url=pres_url,callback=self.res_each_appli)

    def res_each_appli(self,response):
        download_link=response.xpath('//*[@id="soft_list"]/li/a/@href').extract()
        for each_downlink in download_link:
            #print each_downlink
            try:
                yield scrapy.Request(url=each_downlink,callback=self.get_each_download_url)
            except Exception,e:
                print e.message

    def get_each_download_url(self,response):
        download_url=response.xpath('//*[@id="down_url"]/li[1]/a/@href').extract()
        for each_download_url in download_url:
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


