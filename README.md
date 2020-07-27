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
#### 2.3 main.py选择一个爬虫运行
* taobao.py 测试爬虫
* gameDescribe.py  爬取游民星空的测试爬虫
* steam.py   爬取steam网站的爬虫
* TreeDM.py  爬取3DM网站的爬虫
* youmin.py  爬取游民星空网站的爬虫



## 爬取数据格式
不同网站包含的数据，并在后续进行数据的清洗和集成

|  网站   | 数据字段  |
|  ----  | ----  |
| 游民星空  | 游戏网页url 游戏名称 游戏英文名 游戏图片链接 游戏描述 游戏评分 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏玩家评论 游戏攻略链接 游戏时长 游戏标签 |
| steam  | 游戏网页url 游戏名称 游戏图片链接 游戏描述 游戏价格 游戏评价 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏说明 |
| 3DM  | 游戏网页url 游戏名称 游戏英文名 游戏图片链接 游戏描述 游戏评分 游戏人数 游戏发行方 游戏发行时间 游戏类型 游戏下载地址 游戏配置信息 |

本项目提供爬虫爬到的数据：
* gameDescribe.py  -> /data/game_data.csv
* steam.py  -> /data/steam_game_data_desc.csv
* TreeDM.py  -> /data/Tdm_game_data_desc.csv
* youmin.py  -> /data/youmin_game_data_desc.csv


## 爬取数据的清洗和集成

因为不同网站爬取的数据字段不同，并且爬取的数据的中具有空数据和脏数据所以进行数据的清洗和集成。通过/data_process/data_clean.py和data_ Integration.py进行。主要按照数据的特点通过游戏的名称，英文名称进行游戏实体的识别并进行数据的集成。请运行完爬虫后进行再进行数据的清洗和集成。
本项目提供集成后的游戏数据：
* /data/test.csv

## 完整Web数据管理项目
本项目是山东大学软件学院Web数据管理课程设计完整项目的一部分，整体项目包含游戏数据爬取项目，游戏数据前端web项目，以及游戏数据后端项目。本项目有很好的学习价值运用，主要技术特色和应用：

#### 1.GameDataSpider：
Scrapy+selenium+PhantomJS构建出动态页面爬虫程序，爬取了游民星空，Steam,3DM网站的游戏数据并进行星系和集成。https://github.com/SlotherCui/GameDataSpider
#### 2.GameDataManagement：
采用Vue+ Elementui 搭建出游戏数据web前端展示界面，界面美观操作简洁 https://github.com/SlotherCui/GameDataManagement
#### 3.GameDataWeb：
采用Spring-boot+ mysql搭建游戏数据管理后端程序，可以实现多种字段的组合检索 https://github.com/SlotherCui/GameDataWeb

## 说明
*  __本项目采用真实爬取的数据，您可以随意使用，修改和扩展__
*  __本项目包含了简单的Spring-boot后端框架的使用，Vue前端Web框架的使用，MongoDB/Mysql数据库的使用，以及通过python构建爬虫轻松祝您成为技术小佬__
*  __我敢保证只要掌握了本项目，至少对于山东大学软件学院软件工程专业的所有课程设计/实验都都可以轻松快速完成(完全可以套模板)，A+在想你召唤（剩下全靠您实验报告中的吹B）。__
*  __期待你的star__