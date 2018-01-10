import scrapy

from CrawlMacApp.items import CrawlmacappItem

class WwwSkycnComSpider(scrapy.Spider):
    name = "www_33lc_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ['http://www.skycn.com/']

    def start_requests(self):
        s="http://www.33lc.com/index.php?m=lc_search&c=index&a=pc&keywords=mac&pdtc=1&page=1"
        for i in range(1,98):
            base_url="http://www.33lc.com/index.php?m=lc_search&c=index&a=pc&keywords=mac&pdtc=1&page="+str(i)
            #print base_url
            yield scrapy.Request(url=base_url,callback=self.pres_each_page)

    def pres_each_page(self,response):
        all_download_link=response.xpath('//body/div[@id="main1k"]//div[@class="soft_list"]/div[@class="box"]/p/a/@href').extract()
        for each_download_link in all_download_link:
            each_download_link="http://www.33lc.com"+each_download_link
            #print each_download_link
            try:
                yield scrapy.Request(url=each_download_link,callback=self.get_each_download_url)
            except Exception,e:
                print e.message
    def get_each_download_url(self,response):
        download_url=response.xpath('//*[@id="main1k"]/div[5]/div[1]/div[8]/div[2]/div[2]/div/div/div/dl[2]/dd/a[1]/@href').extract()
        for each_download_url in download_url:
            #print each_download_url
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


