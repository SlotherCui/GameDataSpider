# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyseleniumtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name = scrapy.Field()  ##游戏名称
    game_score = scrapy.Field() ##游戏评分
    game_link = scrapy.Field()  ##游戏网址
    game_img = scrapy.Field()   ##游戏图片
    pass

class GameDetailItem(scrapy.Item):

    game_name = scrapy.Field()  ##游戏名称
    game_name_eng = scrapy.Field()  ##游戏名称英文
    game_type = scrapy.Field()  ##游戏类型
    game_time = scrapy.Field()  ##游戏上市时间
    game_author = scrapy.Field()  ##制作发行方
    game_img = scrapy.Field()  ##游戏图片


    game_link = scrapy.Field()  ##游戏网址


    game_score = scrapy.Field()  ##游戏评分
    game_player_num = scrapy.Field()  ##玩家点评数


    game_play_time = scrapy.Field() ##游戏时长
    game_tags = scrapy.Field()   ##玩家常用标签
    game_strategys = scrapy.Field()  ##游戏攻略
    game_describe = scrapy.Field()  ##游戏介绍
    game_player_comments = scrapy.Field()  ##玩家评论

    pass
class SteamItem(scrapy.Item):
    game_name = scrapy.Field()  ##游戏名称
    game_author = scrapy.Field()  # 游戏开发
    game_type = scrapy.Field()  # 游戏类型
    game_time = scrapy.Field()  # 游戏时间
    game_img = scrapy.Field()  ##游戏图片

    game_link = scrapy.Field()  # 游戏网址


    game_comment =  scrapy.Field() #游戏评价
    game_comment_num = scrapy.Field() # 游戏评价

    game_describe = scrapy.Field()  # 游戏介绍
    game_price = scrapy.Field()  # 游戏价格
    game_about = scrapy.Field() # 关于游戏

class ThreeDMtem(scrapy.Item):
    game_name = scrapy.Field()  ##游戏名称
    game_name_en = scrapy.Field()  ##游戏英文名
    game_type = scrapy.Field()  # 游戏类型
    game_time = scrapy.Field()  # 游戏时间
    game_author = scrapy.Field()  # 游戏开发
    game_img = scrapy.Field()  ##游戏图片
    

    game_link = scrapy.Field()  # 游戏网址

    game_score = scrapy.Field()  ##游戏评分
    game_comment_num = scrapy.Field()  # 游戏评价人数

    game_downloader = scrapy.Field()  ##游戏下载
    game_configure = scrapy.Field()  ##游戏配置
    game_describe = scrapy.Field()  # 游戏介绍



class AddItem(scrapy.Item):
    # game_name = scrapy.Field()  ##游戏名称
    # game_name_eng = scrapy.Field()  ##游戏名称英文
    # game_link = scrapy.Field() # 游戏网址

    game_link = scrapy.Field()  # 游戏网址
    game_img = scrapy.Field()  ##游戏图片

