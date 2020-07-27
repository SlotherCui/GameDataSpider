# -*- coding: utf-8 -*-
import scrapy
from ..items import SteamItem

class SteamSpider(scrapy.Spider):
    name = 'steam'
    # allowed_domains = ['https://store.steampowered.com/games/?l=schinese#p=']
    # start_urls = ['https://store.steampowered.com/games/?l=schinese#p=0&tab=ConcurrentUsers']
    start_urls = ['']


    def __init__(self):
        self.page = 1                                 # 记录爬取页数
        self.cookies = {'lastagecheckage': '1-0-1998',
                        'steamCountry':'"CN%7Cc29a4204822c80e40536083b1124ff87"',
                        'birthtime':'880905601'}
        super(SteamSpider, self).__init__()

    def parse(self, response):

        # yield scrapy.Request('https://store.steampowered.com/bundle/8538/Devil_May_Cry_5__Deluxe_Edition/?snr=1_7_7_230_150_8&l=schinese', cookies=self.cookies, callback=self.parseDetail)  # 继续访问该URL并翻页

        # 获取游戏列表
        game_list = response.xpath("//div[@id='search_result_container']/div[2]/a")
        for game in game_list:
            # 抽取游戏介绍页面url
            url = game.xpath("./@href").extract_first()+"&l=schinese"
            print(url)

            # 进入每个游戏详情页面爬取 （并行）
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parseDetail,dont_filter = False)  # 继续访问该URL并翻页

        # 页数加一
        self.page+=1
        print(self.page)

        # 没有到最后一页
        if self.page<2284:
            # 爬取下一页的游戏列表
            yield scrapy.Request('https://store.steampowered.com/search/?sort_by=Name_ASC&page='+str(self.page),
                                 callback=self.parse,dont_filter = True)

    # 抽取游戏详情页面的数据
    def parseDetail(self, response):
        # print(response.url)
        gameItem = SteamItem()

        # 游戏网页URL
        gameItem['game_link'] = response.url

        # 游戏名称
        gameItem['game_name'] = response.xpath("//div[@class='apphub_AppName']/text()").extract_first()

        if gameItem['game_name']!=None:

            # 游戏介绍
            gameItem['game_describe'] = response.xpath("//div[@class='game_description_snippet']/text()").extract_first()
            # 游戏图片
            gameItem['game_img'] = response.xpath("//img[@class='game_header_image_full']/@src").extract_first()

            # 游戏价格
            try:   # 处理减价情况
                gameItem['game_price'] = \
                    response.xpath("//div[@class='game_purchase_price price']/text()")\
                        .extract_first().replace("\r\n","").replace("\t","")
            except:
                gameItem['game_price'] = \
                    response.xpath("//div[@class='discount_original_price']/text()")\
                        .extract_first()

            # 游戏你评价
            gameItem['game_comment'] = response.xpath("//div[@class='summary_section']/span[1]/text()").extract_first()
            # 游戏人数
            gameItem['game_comment_num'] = response.xpath("//div[@class='summary_section']/span[2]/text()").extract_first()
            # 游戏发行方
            gameItem['game_author'] = response.xpath("//div[@class='summary column']/a/text()").extract_first()
            # 游戏类型
            gameItem['game_type'] = response.xpath("//div[@class='details_block'][1]/a/text()").extract()
            # 游戏发行时间
            gameItem['game_time'] = response.xpath("//div[@class='date']/text()").extract_first()
            # 游戏说明
            gameItem['game_about'] = response.xpath("//div[@class='game_area_description']/text()").extract()

            # print(gameItem)

        else:
            gameItem['game_img'] = response.xpath("//img[@class='package_header']/@src").extract_first()
            gameItem['game_name'] = response.xpath("//h2[@class='pageheader']/text()").extract_first()
            gameItem['game_describe'] = "特殊游戏/捆绑包"
            print('有点问题')

        yield gameItem