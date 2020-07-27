import pymongo


def transfrom_tdm_score(tdm_score):
    if tdm_score != "" and tdm_score != '0.0':
        tdm_score = float(tdm_score) / 2
    else:
        tdm_score = 0.0
    return tdm_score

def transfrom_tdm_comment_num(tdm_score):
    if tdm_score==None or tdm_score=="":
        return 0
    else:
        return int(tdm_score)

comment_dict = {"好评如潮":5.0,"特别好评":4.5,"好评":4.0,"多半好评":3.5,
                "褒贬不一":3.0,"多半差评":2.5,"差评":2.0,"特别差评":1.5,"差评如潮":1.0}
def transfrom_steam_comment(comment):
    if comment in comment_dict:
        return comment_dict[comment]
    else:
        return 0.0
def transfrom_steam_comment_num(comment_num):
    if comment_num==None or comment_num=="":
        return 0
    else:
        return int(comment_num[1:-5].replace(",",""))

def avg_score(scores):
    times = 0
    sum_score=0.0
    for score in scores:
        if score=="--" or score=="":
            pass
        else:
            sum_score+=score
            times+=1

    if times>0:
        return round(sum_score/times,2)
    else:
        return 0.0



def transform(name):
    if name !=None:
        name = name.replace(" ","")     # 去除空格冒号
        name = name.replace(":","")
        name = name.replace("：", "")
        name = name.replace("®", "")    #去除特殊符号
        name = name.replace("™", "")
        name = name.replace("-", "")
        name = name.replace("&", "")
        name = name.replace("IV","4")   # 罗马数字转数字
        name = name.replace("V", "5")
        name = name.replace("III", "3")
        name = name.replace("II", "2")
        return name.lower()
    else:
        return name

def get(v,key):
    if key in v and v[key]!=None:
        return v[key]
    else:
        return ""


def transform_time(time):
    if time=="" or time==None:
        return "未知"
    else:
        time = time.replace("年", "-")
        time = time.replace("月", "-")
        time = time.replace("日", "")
        return time

    pass


def InitData(v):
    data={}
    data['game_name'] = get(v,'game_name')
    data['game_type'] = get(v, 'game_type')
    data['game_time'] = transform_time(get(v, 'game_time'))
    data['game_author'] = get(v, 'game_author')
    data['game_avg_score'] = get(v, 'game_score')
    data['game_sum_player'] = get(v, 'game_comment_num')
    data['game_img'] = get(v, 'game_img')
    data['youmin_link'] = ""
    data['tdm_link'] = ""
    data['steam_link'] = ""
    return data



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



# 将所有数据直接读到内存中  用空间换时间
steam_data_dict = {}
steam_data = steam_post.find()
for data in steam_data:
    name = transform(data['game_name'])
    steam_data_dict[name]=dict(data)

print(len(steam_data_dict))
print()
tdm_data_dict = {}
tdm_data_dict2 = {}
tdm_data = tdm_post.find()
for data in tdm_data:
    if 'game_name_en' in data:
        name = transform(data['game_name_en'])
        tdm_data_dict[name]=dict(data)

    tdm_data_dict2[data['game_name']] = dict(data)
print(len(tdm_data_dict))
print(len(tdm_data_dict2))
print()
youmin_data_dict = {}
youmin_data= youmin_post.find()
for data in youmin_data:
    if 'game_name_eng' in data:
        youmin_data_dict[data['game_name_eng']]=dict(data)

print(len(youmin_data_dict))
print()
links = set() # 记录出现过的链接count
data_integration = [] # 集成结果数据


# game_name 作为主键连接 三个数据集

count = 0

for k in youmin_data_dict:

    v = youmin_data_dict[k]
    data = InitData(v)
    data['game_name_eng'] = get(v,'game_name_eng')
    data['youmin_link'] = get(v,'game_link')
    data['game_sum_player'] = int(get(v, 'game_player_num'))



    # data['game_avg_score'] = get(v, 'game_score')
    if data['game_avg_score'] !='--':
        data['game_avg_score']= float(data['game_avg_score'])/2
    links.add(data['youmin_link'])

    # 与steam英文名进行匹配
    steam_score = "--"
    name = transform(data['game_name_eng'])
    if name in steam_data_dict:
        steam_link = steam_data_dict[name]['game_link']
        if steam_link not in links:
            data['steam_link'] = steam_link
            # 获得steam得分
            steam_score = transfrom_steam_comment(get(steam_data_dict[name],"game_comment"))
            links.add(steam_link)
            count+=1
            # 获得steam游戏人数
            steam_player_num = transfrom_steam_comment_num(get(steam_data_dict[name],"game_comment_num"))
            data['game_sum_player']+=steam_player_num

    else:
        data['steam_link'] = ""


    # 与3dm英文名进行匹配
    tdm_score = "--"
    if name in tdm_data_dict:
        tdm_link = tdm_data_dict[name]['game_link']
        data['tdm_link'] = tdm_link
        count += 1
        # 获得3dm得分
        tdm_score = transfrom_tdm_score(get(tdm_data_dict[name], "game_score"))

        # 获得3dm人数
        tdm_player_num = transfrom_tdm_comment_num(get(tdm_data_dict[name], "game_comment_num"))

        data['game_sum_player'] += tdm_player_num

        links.add(tdm_link)

    # 与3dm中文名进行匹配

    if data['game_name'] in tdm_data_dict2:
        tdm_link = tdm_data_dict2[data['game_name']]['game_link']
        if tdm_link not in links:
            data['tdm_link'] = tdm_link
            # 获得3dm得分
            tdm_score =transfrom_tdm_score(get(tdm_data_dict2[data['game_name']], "game_score"))
            count += 1
            # 获得3dm人数
            tdm_player_num = transfrom_tdm_comment_num(get(tdm_data_dict2[data['game_name']], "game_comment_num"))
            data['game_sum_player'] += tdm_player_num


            links.add(tdm_link)

    data['game_avg_score'] = avg_score([data['game_avg_score'],steam_score,tdm_score])
    data_integration.append(data)


print(len(data_integration))
print(len(links))

for k in tdm_data_dict:
    v = tdm_data_dict[k]
    data = InitData(v)
    data['tdm_link'] = v['game_link']
    # 没有出现过的3DM
    if data['tdm_link'] not in links:
        data['game_name_eng'] = get(v,'game_name_en')

        links.add(data['tdm_link'])
        name = transform(data['game_name_eng'])
        # 获得3dm得分
        data['game_avg_score'] = transfrom_tdm_score(get(v, "game_score"))
        # 获得3dm人数
        data['game_sum_player'] = transfrom_tdm_comment_num(get(v, "game_comment_num"))


        # 是否在steam中
        if name in steam_data_dict:
            steam_link = steam_data_dict[name]['game_link']
            if steam_link not in links:
                data['steam_link'] = steam_link
                count += 1
                # 获得steam得分
                steam_score = transfrom_steam_comment(get(steam_data_dict[name], "game_comment"))
                data['game_avg_score'] = avg_score([data['game_avg_score'], steam_score])

                # 获得steam游戏人数
                steam_player_num = transfrom_steam_comment_num(get(steam_data_dict[name], "game_comment_num"))
                data['game_sum_player'] += steam_player_num


                links.add(steam_link)
        data_integration.append(data)

print(len(data_integration))
print(len(links))
# 没有出现过的3dm游戏
for k in tdm_data_dict2:
    v = tdm_data_dict2[k]
    data = InitData(v)
    data['tdm_link'] = v['game_link']
    # 没有出现过的3DM
    if data['tdm_link'] not in links:
        data['game_name_eng'] = get(v, 'game_name_en')
        # 获得3dm得分
        data['game_avg_score'] = transfrom_tdm_score(get(v, "game_score"))
        # 获得3dm人数
        data['game_sum_player'] = transfrom_tdm_comment_num(get(v, "game_comment_num"))

        links.add(data['tdm_link'])
        data_integration.append(data)

print("here")
print(len(data_integration))
print(len(links))

# 没有出现过的steam游戏
for k in steam_data_dict:
    v = steam_data_dict[k]
    data = InitData(v)
    data['steam_link'] = v['game_link']
    # 没有出现过的steam游戏
    if data['steam_link'] not in links:
        data['game_name_eng'] = v['game_name']

        # 获得steam得分`
        data['game_avg_score'] = transfrom_steam_comment(get(v, "game_comment"))
        # 获得steam人数
        data['game_sum_player'] = transfrom_steam_comment_num(get(v, "game_comment_num"))

        data['game_type'] = " ".join(data['game_type'])
        if data['game_type']==""and get(v, "game_describe")=="特殊游戏/捆绑包":
            data['game_type'] = "特殊游戏/捆绑包"

        links.add(data['steam_link'])
        data_integration.append(data)



print(len(data_integration))
print(len(links))
print(count)
#

# test = db['test']
# test.insert_many(data_integration)



#
# youmin_steam = youmin_post.find()



