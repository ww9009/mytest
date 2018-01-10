import scrapy

from CrawlMacApp.items import CrawlmacappItem

class Www3987ComSpider(scrapy.Spider):
    name = "www_3987_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ['http://download.cnet.com/most-popular/mac/']
    #base_url = 'http://download.cnet.com/s/software/mac/?sort=most-popular&page='
    def start_requests(self):
        for i in range(2,97):
            avail_url="https://www.3987.com/xiazai/html/mac_"+str(i)+".html"
            yield scrapy.Request(url=avail_url,callback=self.parse)
    def parse(self, response):
        all_doanload_pages=response.xpath('//*[@id="tabnew_0"]/ul/li/a[2]/@href').extract()
        for each_download_page in all_doanload_pages:
            each_download_page="https:"+each_download_page
            yield scrapy.Request(url=each_download_page,callback=self.get_each_app_url)

    def get_each_app_url(self,response):
        all_apps_download_urls=response.xpath('//*[@id="down"]/div[2]/div[1]/ul[2]/li[1]/a/@href').extract()
        soft_id=response.xpath('//*[@id="down"]/div[2]/div[1]/ul[2]/li[1]/a/@data').extract()[0]
        for each_app_d_url in all_apps_download_urls:
            print each_app_d_url
            item = CrawlmacappItem()
            item['soft_id'] = "www_3987_"+soft_id
            item['soft_name'] = ""
            item['download_link'] = each_app_d_url
            item['is_download'] = False
            item['download_time'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = ""
            yield item

