# -*- coding: utf-8 -*-
import scrapy
from ..items import ScrapyseleniumtestItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class YouminSpider(scrapy.Spider):
    name = 'youmin'                                #爬虫名
    allowed_domains = ['ku.gamersky.com/sp/']      #爬虫允许的URL范围
    start_urls = ['http://ku.gamersky.com/sp/']    #爬虫开始URL
    # 爬虫初始化函数
    def __init__(self):
        self.browser = webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1-windows/bin/phantomjs.exe')     #selenium 加载PhantomJS驱动
        self.isfirst = False                                                                                   #第一次访问不翻页
        super(YouminSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    #爬虫关闭
    def spider_closed(self, spider):
        print('spider closed')
        self.browser.quit()

    # 网页数据解析
    def parse(self, response):

        # 获取游戏列表
        game_list = response.xpath("//div[@class='Mid']//ul/li")

        for game in game_list:
            gameItem = ScrapyseleniumtestItem()
            gameItem['game_name'] = game.xpath(".//div//p/text()").extract_first()      # 游戏名称
            gameItem['game_score'] = game.xpath(".//div//div/text()").extract_first()   # 游戏评分
            gameItem['game_link'] = game.xpath(".//div//a/@href").extract_first()       # 游戏介绍页面URL
            gameItem['game_img'] = game.xpath(".//div//img/@src").extract_first()       # 游戏封面图片链接
            print(gameItem)
            yield gameItem

        self.isfirst = True        # 标记可以翻页

        yield scrapy.Request('http://ku.gamersky.com/sp/', callback=self.parse, dont_filter = True)    # 继续访问该URL并翻页

