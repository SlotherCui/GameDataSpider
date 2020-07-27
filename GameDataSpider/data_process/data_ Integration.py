import pymongo


# 将三个数据源爬取的数据进行集成合并到一个Mogondb collection中


def get(v,key):
    if key in v and v[key]!=None:
        return v[key]
    else:
        return ""


# mongodb 数据库链接信息
mongo_host = 'localhost'
mongo_port = 27017
mongo_db_name = 'spider'

# 连接mongodb数据库
client = pymongo.MongoClient(host=mongo_host, port=mongo_port)
db = client[mongo_db_name]


# 来自三个数据源的数据
steam_post = db['steam_game_data_desc']
tdm_post = db['Tdm_game_data_desc']
youmin_post = db['game_data_desc']

steam_data = steam_post.find()
steam_data_clean = []
for data in  steam_data:
    rowdata = {}
    rowdata['game_link'] =  get(data,'game_link')
    rowdata['game_price'] =  get(data,'game_price')
    rowdata['game_describe'] =  get(data,'game_describe')
    rowdata['game_about'] = "\n".join(get(data,'game_about'))
    rowdata['game_img'] = get(data, 'game_img')
    steam_data_clean.append(rowdata)

test = db['test_steam_data2']
test.insert_many(steam_data_clean)
print(len(steam_data_clean))

tdm_data = tdm_post.find()
tdm_data_clean = []
for data in tdm_data:
    rowdata = {}
    rowdata['game_link'] = get(data, 'game_link')
    rowdata['game_downloader'] = get(data, 'game_downloader')
    rowdata['game_describe'] = get(data, 'game_describe')
    rowdata['game_configure'] = str(get(data, 'game_configure'))
    # print(rowdata['game_configure'])
    rowdata['game_img'] = get(data, 'game_img')
    tdm_data_clean.append(rowdata)

test = db['test_tdm_data']
test.insert_many(tdm_data_clean)
print(len(tdm_data_clean))


youmin_data= youmin_post.find()
youmin_data_clean = []
for data in youmin_data:
    rowdata = {}
    rowdata['game_link'] = get(data, 'game_link')
    rowdata['game_play_time'] = get(data, 'game_play_time')
    rowdata['game_tags'] = str(get(data, 'game_tags'))
    rowdata['game_describe'] = "\n".join(get(data, 'game_describe'))
    rowdata['game_player_comments'] = str(get(data, 'game_player_comments'))
    rowdata['game_strategys'] = str(get(data, 'game_strategys'))
    rowdata['game_img'] = get(data, 'game_img')
    youmin_data_clean.append(rowdata)
test = db['test_youmin_data']
test.insert_many(youmin_data_clean)
print(len(youmin_data_clean))
#
# with open('C://Users//Sloth//Desktop//test_youmin_data_test.csv',"r",encoding='utf-8') as f:    #设置文件对象
#     str = f.read()    #可以是随便对文件的操作
#     print(len(str))
#


