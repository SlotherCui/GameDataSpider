# -*- coding: utf-8 -*-
import scrapy
from ..items import ThreeDMtem
from ..items import AddItem
class TreedmSpider(scrapy.Spider):
    name = 'TreeDM'
    allowed_domains = ['dl.3dmgame.com/']
    start_urls = []

    def __init__(self):
        self.page = 1  # 记录爬取页数
        self.start_urls.append('https://dl.3dmgame.com/all_all_'+str(self.page)+'_hot/')
        super(TreedmSpider, self).__init__()

    def parse(self, response):

        # 获取游戏列表
        game_list = response.xpath("//ul[@class='downllis']/li")

        for game in game_list:
            # 抽取游戏介绍页面url
            url = game.xpath("./div/a[@class='a_click']/@href").extract_first()

            # 爬取游戏介绍页面的内容
            yield scrapy.Request(url, callback=self.parseDetail, dont_filter=True)

        # 进入下一页
        self.page+=1
        if self.page<1828:
            yield scrapy.Request('https://dl.3dmgame.com/all_all_'+str(self.page)+'_hot/', callback=self.parse, dont_filter=True)

        # game_item = AddItem()
        # game_item['game_link'] = url
        # game_item['game_img'] = game.xpath("./div/div[@class='img']//a/img/@src").extract_first()
        # yield game_item

        # print(url)
    def parseDetail(self, response):
        game_item = ThreeDMtem()
        name = response.xpath("//div[@class='name']/h1/text()").extract_first()
        game_item['game_link'] = response.url

        game_list = response.xpath("//ul[@class='list']/li")
        # 游戏类型
        game_item['game_type'] = game_list[0].xpath("./span/text()").extract_first()
        # 游戏发行方
        game_item['game_author'] = game_list[1].xpath("./span/text()").extract_first()
        # 游戏发行时间
        game_item['game_time'] = game_list[2].xpath("./span/text()").extract_first()

        # 游戏评分
        game_item['game_score'] = response.xpath("//div[@class='processingbar']/font/text()").extract_first()
        # 游戏描述
        game_item['game_describe'] = response.xpath("//div[@class='GmL_1']/p[1]/text()").extract_first()

        # 游戏下载地址
        game_item['game_downloader'] =  "http://id.ttz9.cn/thn/"+name+"_id372@372_1"+response.url.split("/")[-1][:-5]

        # 游戏配置
        table = response.xpath("//div[@class='GmL_2']//table//tbody/tr")
        game_item['game_configure'] = []
        for tr in table:
            tds = tr.xpath("./td/text()").extract()
            Row = {tds[0]:tds[1]+"@"+tds[2]}
            game_item['game_configure'].append(Row)

        # 游戏评论人数
        game_item['game_comment_num'] = response.xpath("//span[@class='num1']/text()").extract_first()


        # 游戏名称抽取







        if "《" in name:
            game_item['game_name'] = name[name.find("《")+1:name.find("》")]
        else:
            game_item['game_name'] = ' '.join(name.split(" ")[:-1])
            # print(name)
            print(game_item['game_name'])

        # 游戏英文名称抽取
        game_name_en  = response.xpath("//div[@class='name']/a/i/text()").extract_first()
        if game_name_en!=None:  # 判定存在
            game_item['game_name_en'] = game_name_en[1:-1] # 去除括号

        yield game_item

        # print(eng_name)
        # if eng_name!=None:
        #     print(eng_name)
        # else:
        #     describe = game_item['game_describe']

        #     print()
        # print(game_item)

        # game_describe = response.xpath("//div[@class='GmL_1']/p[1]/text()").extract_first()
        # if game_describe=="游戏简介：":
        #     game_item['game_describe'] = response.xpath("//div[@class='GmL_1']/p[2]/text()").extract_first()
        #
        # else:
        #     game_item['game_describe'] = game_describe

    #     # print(name)
