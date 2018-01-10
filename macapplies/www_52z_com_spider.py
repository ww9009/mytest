import scrapy
import re
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem

class Www52zComSpider(scrapy.Spider):
    name = "www_52z_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ["http://www.52z.com/soft/343810.html#softdown"]
    #base_url="http://www.52z.com"

    def start_requests(self):
        sou_file="/home/smallchild/sample_crawler_master_ww/CrawlMacApp/tmp.txt"
        t_f=open(sou_file,'r')
        for each_url in t_f.readlines():
            prs_url=each_url.split("\n")[0]
            yield SplashRequest(url=prs_url,callback=self.parse)
        # prs_url="http://www.52z.com/soft/343810.html#softdown"
        # yield SplashRequest(url=prs_url,callback=self.parse)
    def parse(self, response):
        print response.url

        download_urls = response.xpath('//*[@id="downajaxview"]/div[2]/ul/li[2]/a[@class="icon2 ywAblack"]/@href').extract()
        for each_download_url in download_urls:
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




'''
    def parse(self, response):
        all_categories=response.xpath('/html/body/div[3]/div[2]/div[1]/ul/li[1]/div[2]/a/@href').extract()
        all_category_num=response.xpath('/html/body/div[3]/div[2]/div[1]/ul/li[1]/div[2]/a/@title').extract()

        for i in range(len(all_categories)):
            each_category_url="http://www.52z.com/SoftList/"+all_categories[i]
            pattern=re.compile(r'.*?(\d+).*')
            total_num=pattern.findall(all_category_num[i])[0]

            yield scrapy.Request(url=each_category_url,callback=self.pres_gouzao_url,meta={"totalnum":total_num})

    def pres_gouzao_url(self,response):
        total_num=response.meta["totalnum"]
        tmp_total_page=int(total_num)/20
        if tmp_total_page*20==total_num:
            total_page=tmp_total_page
        else:
            total_page=tmp_total_page+1


        for i in range(1,total_page+1):
            if i==1:
                pres_url=response.url
            else:
                tmp=response.url.split('_')[0]
                pres_url=tmp+"_"+str(i)+".html"
            yield scrapy.Request(url=pres_url,callback=self.get_all_download_link)
    def get_all_download_link(self,response):
        downloads_links=response.xpath('/html/body/div[3]/div[3]/div[1]/ul/li/dl/dt/a/@href').extract()
        for each_download_link in downloads_links:
            each_download_link=self.base_url+each_download_link
            try:
                yield scrapy.Request(url=each_download_link,callback=self.get_each_download_url)
            except Exception,e:
                print e.message


    def get_each_download_url(self,response):
        print response.url

        t_f=open("tmp.txt","a+")
        t_f.write(response.url+"\n")


        download_urls=response.xpath('//*[@id="downajaxview"]/div[2]/ul/li[1]/a/@href').extract()
        print len(download_urls)
        allow_postfix=('.dmg','.zip','.tar','.pkg')
        if len(download_urls)>0:
            for each_download_url in download_urls:
                if each_download_url.endswith(allow_postfix):
                    pass
                # item = CrawlmacappItem()
                # item['soft_id'] = each_download_url
                # item['soft_name'] = ""
                # item['download_link'] = each_download_url
                # item['is_download'] = False
                # item['download_time'] = ""
                # item['is_upload_ftp'] = False
                # item['upload_time'] = ""
                # item['upload_file_name'] = ""
                # item['download_http_error'] = False
                # item['soft_desc'] = ""
                # yield item
'''
