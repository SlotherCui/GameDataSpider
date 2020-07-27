# GameDataSpider
 一个基于Scrapy游戏数据爬虫项目 Game Data Sprider。本项目基于Scrapy构建的爬虫项目并爬取截止到2019年4月之前的steam，游民星空，3dm三个网站的游戏数据存储到MongoDB数据库中，并采用selenium+PhantomJS下载器中间件进行动态界面进行爬取，最后本项目对爬取到的数据并进行数据的清洗和集成。

## 运行配置
### 1. 基础环境配置
#### 1.1 安装配置python3环境
#### 1.2 安装Scrapy selenium PhantomJS
#### 1.3 安装配置MogoDB数据库
### 2. 配置运行
#### 2.1 配置pipelines.py的MogoDB的链接配置
#### 2.2 setting.py 跟据需求修改Scrapy相关配置
#### 2.3 main.py选择一个爬虫进行运行

## 爬取数据格式
不同网站包含的数据，并在后续进行数据的清洗和集成

|  网站   | 数据字段  |
|  ----  | ----  |
| 游民星空  | 游戏网页url 游戏名称 游戏英文名 游戏图片链接 游戏描述 游戏评分 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏玩家评论 游戏攻略链接 游戏时长 游戏标签 |
| steam  | 游戏网页url 游戏名称 游戏图片链接 游戏描述 游戏价格 游戏评价 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏说明 |
| 3DM  | 游戏网页url 游戏名称 游戏英文名 游戏图片链接 游戏描述 游戏评分 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏下载地址 游戏配置信息 |

本项目提供爬虫爬到的数据：
gameDescribe.py  -> /data/game_data.csv
steam.py  -> /data/steam_game_data_desc.csv
TreeDM.py  -> /data/Tdm_game_data_desc.csv
youmin.py  -> /data/youmin_game_data_desc.csv


## 爬取数据的清洗和集成

因为不同网站爬取的数据字段不同，并且爬取的数据的中具有空数据和脏数据所以进行数据的清洗和集成。通过/data_process/data_clean.py和data_ Integration.py进行。主要按照数据的特点通过游戏的名称，英文名称进行游戏实体的识别并进行数据的集成。请运行完爬虫后进行再进行数据的清洗和集成。
本项目提供集成后的游戏数据：
/data/test.csv

## 完整Web数据管理项目