# -*- coding: utf-8 -*-
import scrapy
from ..items import GameDetailItem
from ..items import AddItem
import  pymongo
class GamedescribeSpider(scrapy.Spider):
    name = 'game_describe'
    allowed_domains = ['ku.gamersky.com/']
    start_urls = []

    def __init__(self):

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["spider"]
        mycol = mydb["game_data"]
        for x in mycol.find():
            self.start_urls.append(x['game_link'])     # 从MongoDB读出游戏界面url

        start = 0
        self.start_urls = self.start_urls[start:]      # 设置开始点，以便增量爬取。

        self.count = 0                                 # 记录爬取了几个URL
        super(GamedescribeSpider, self).__init__()



    def parse(self, response):
        # gameItem = AddItem()

        gameItem = GameDetailItem()

        # 游戏英文名称
        gameItem['game_name_eng'] = response.xpath("// div[@class ='tit_EN']/text()").extract_first()

        # 游戏网页url
        gameItem['game_link']= response.url

        # print(gameItem)



        # 游戏名称
        gameItem['game_name'] = response.xpath("// div[@class ='tit_CH']/text()").extract_first()

        # 游戏评分
        score = response.xpath("//div[@class ='num']/i/@class").extract()
        if len(score)==3:
            gameItem['game_score'] =score[0][1:]+'.'+score[2][1:]
        else :
            gameItem['game_score'] = '--'

        # 游戏图片链接
        gameItem['game_img'] = response.xpath("// div[@class ='img']//a/img/@src").extract_first()

        # 游戏类型
        gameItem['game_type'] = response.xpath("// div[@class ='tag']//a/text()").extract_first()
        # 游戏上市时间
        gameItem['game_time'] =response.xpath("//div[@class ='tt1']//div[@class='time']/text()").extract_first()
        # 游戏时长
        gameItem['game_play_time'] =response.xpath("//div[@class ='clock']/text()").extract_first().replace("\n", "").strip()
        # 制作发行方
        gameItem['game_author'] =  response.xpath("//div[@class ='div3']//div[@class='tt2']//div[@class='txt']/text()").extract_first()
        # 玩家点评数
        gameItem['game_player_num'] = response.xpath("//span[@id ='scoreTimes']/text()").extract_first()
        # 游戏介绍
        gameItem['game_describe']=response.xpath("//div[@class ='con']/p/text()").extract()
        # 玩家常用标签
        gameItem['game_tags'] = response.xpath("//div[@class ='WJCYtag']//span/a/text()").extract()

        # 游戏攻略
        names = response.xpath("//ul[@class='titlist']/li/a/text()").extract()
        links = response.xpath("//ul[@class='titlist']/li/a/@href").extract()
        gameItem['game_strategys'] = []
        for i in range(len(names)):
            map = {'strategy_name':names[i],'strategy_link':links[i]}
            gameItem['game_strategys'].append(map)

        # 玩家评论
        game_comments =response.xpath("//div[@class='remark-list-cont']/div[@class='remark-list-floor']")
        comments =  []
        for comment in game_comments:
            comments.append(comment.xpath(".//div[@class='content']/text()").extract_first().replace('\t','').replace('\n',''))
        gameItem['game_player_comments'] = comments

        # 记录爬取程度
        self.count= self.count+1;
        print(self.count)

        # 保存数据
        yield gameItem

