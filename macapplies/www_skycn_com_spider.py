import scrapy

from CrawlMacApp.items import CrawlmacappItem

class WwwSkycnComSpider(scrapy.Spider):
    name = "www_skycn_com_soider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    start_urls = ['http://www.skycn.com/']

    def parse(self, response):
        all_categories=response.xpath('//*[@id="j_left_nav"]/ul/li/ul/li/a/@href').extract()
        total_num=response.xpath('//*[@id="j_left_nav"]/ul/li/ul/li/a/i[@class="ext"]/text()').extract()
        for i in range(len(all_categories)):
            #print all_categories[i]
            total_num_1 = int(total_num[i][1:-1])

            yield scrapy.Request(url=all_categories[i],callback=self.pres_each_category,meta={"total_num":total_num_1})

    def pres_each_category(self,response):
        total_num = response.meta["total_num"]

        tmp = total_num / 10
        if tmp * 10 == total_num:
            total_pages = tmp
        else:
            total_pages = tmp + 1
        for page in range(1, total_pages + 1):
            if page == 1:
                page_url = response.url
            else:
                tmp_url = response.url.split(".html")[0]
                page_url = tmp_url + "_" + str(page) + ".html"

            try:
                #print page_url
                yield scrapy.Request(url=page_url, callback=self.pres_each_page)
            except Exception, e:
                print e.message

    def pres_each_page(self,response):
        allow_postfix = ('.pkg', '.dmg', '.zip', '.rar')
        all_download_urls=response.xpath('/html/body/div[1]/div[4]/div[2]/div[3]/ul/li/div[2]/a/@href').extract()
        for each_download_url in all_download_urls:
            print each_download_url
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

