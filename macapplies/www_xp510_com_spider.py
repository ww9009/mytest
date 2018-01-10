import scrapy
from scrapy_splash import SplashRequest
from CrawlMacApp.items import CrawlmacappItem

class WwwXp510ComSpider(scrapy.Spider):
    name = "www_xp510_com_spider"
    download_delay = 0
    #allowed_domains = ["download.cnet.com"]
    #start_urls = ['http://www.xp510.com/mac/xtrj.html']
    #base_url = 'http://download.cnet.com/s/software/mac/?sort=most-popular&page='

    def start_requests(self):
        sou_file="/home/smallchild/sample_crawler_master_ww/CrawlMacApp/tmp1.txt"
        t_f=open(sou_file,'r')
        for each_url in t_f.readlines():
            prs_url=each_url.split("\n")[0]
            yield scrapy.Request(url=prs_url,callback=self.parse)

        # prs_url="https://www.xp510.com/mac/yyqt_2.html"
        # yield scrapy.Request(url=prs_url,callback=self.parse)

    def parse(self, response):
        download_url = response.xpath('//body/div[@class="main"]//div[@class="c-box"]/div[@class="c-soft-list"]/ul/li/div[@class="item"]/div[@class="down"]/a/@href').extract()
        # tmp_soft_id=response.xpath('//body/div[@class="main"]//div[@class="c-box"]/div[@class="c-soft-list"]/ul/li/div[@class="top-tit"]/p/a/@href').extract()[0]
        # tmp_soft_id_1=tmp_soft_id.split('/')[4].split('.')[0]
        for each_download_url in download_url:
            #print each_download_url

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
        all_titles=response.xpath('/html/body/div[3]/div[3]/div[1]/div[2]/a/@href').extract()
        for each_title in all_titles[1:]:
            each_title_url="https:"+each_title
            #print each_title_url
            yield scrapy.Request(url=each_title_url,callback=self.pars_each_title)

    def pars_each_title(self,response):

        total_num=response.xpath('//body//div[@class="content"]/div[@class="c-box"]/div[@class="c-soft-list"]/div[@class="page"]/a[1]/text()').extract()
        try:
            total_num=total_num[0]
            avail_download_num=total_num[:-1]
            tmp=int(avail_download_num)/15
            if tmp * 15 == avail_download_num:
                total_pages=tmp
            else:
                total_pages=tmp+1
            for page in range(1,total_pages+1):
                if page==1:
                    page_url=response.url
                else:
                    tmp_url=response.url.split(".html")[0]
                    page_url=tmp_url+"_"+str(page)+".html"

                #print page_url
                yield scrapy.Request(url=page_url,callback=self.pres_each_apply)
        except Exception,e:
            print e.message

    def pres_each_apply(self,response):
        print response.url

        try:
            download_url=response.xpath('//body/div[@class="main"]//div[@class="c-box"]/div[@class="c-soft-list"]/ul/li/div[@class="item"]/div[@class="down"]/a/@href').extract()[0]
            # tmp_soft_id=response.xpath('//body/div[@class="main"]//div[@class="c-box"]/div[@class="c-soft-list"]/ul/li/div[@class="top-tit"]/p/a/@href').extract()[0]
            # tmp_soft_id_1=tmp_soft_id.split('/')[4].split('.')[0]
            print download_url
            #print tmp_soft_id_1
            allow_postfix = ('.dmg', '.zip', '.tar', '.pkg')
            if download_url.endswith(allow_postfix):
                item = CrawlmacappItem()
                item['soft_id'] = download_url
                item['soft_name'] = ""
                item['download_link'] = download_url
                item['is_download'] = False
                item['download_time'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = ""
                yield item

            #print download_url
        except Exception,e:
            print e.message
    '''








