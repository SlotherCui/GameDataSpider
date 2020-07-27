# -*- coding: utf-8 -*-
import scrapy


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['www.taobao.com']
    start_urls = ['http://www.zycg.gov.cn/article/show_for_print?id=537222']



    def parse(self, response):
        print(response.text)
        pass
