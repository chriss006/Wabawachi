import numpy as np
import pandas as pd
import random, re
from pymongo import MongoClient
client = MongoClient("mongodb://chriss:1234@3.38.2.131:27017")
db = client['winedb']


def preprocess_doc():
    docs = db.wine_db.find({},{'_id':0, 'wine_id':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 })
    doc = pd.DataFrame(docs, columns=['wine_id','sweet','acidic','body','tannic'])
    return doc

#similar wine celler 
def get_attributes(wine_id, wines):
    fields = {'_id':0, 'wine_id':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 }
    input_vec = list(db.wine_db.find_one({'wine_id':wine_id},fields).values())
    docs = db.wine_db.find({'wine_id':{'$in':wines}},fields)
    docs =pd.DataFrame(docs, columns=['wine_id','sweet','acidic','body','tannic'])
    
    return input_vec, docs

def find_similar_wine_celler(input_vec, docs):
    dist={}

    for i in docs.index:
        if input_vec[0]!=i: 
            temp = docs.loc[i,['sweet','acidic','body','tannic']]
            dist[int(docs.loc[i,'wine_id'])]=np.sum(np.square(input_vec[1:] - temp.to_numpy()))

    if len(dist)>=5:
        dist = dict(sorted(dist.items(), key= lambda x:x[1])[:5])
    else:
        dist = dict(sorted(dist.items(), key= lambda x:x[1]))

    return(list(dist.keys()))

#simialr wine all 
def find_similar_wine(input_vec, doc):
    dist={}

    for i in doc['wine_id']:
        if input_vec[0][0]!=i: 
            temp = doc.loc[i,['sweet','acidic','body','tannic']]
            dist[i]=np.sum(np.square(input_vec[0][1:] - temp.to_numpy()))

    if len(dist)>=5:
        dist = dict(sorted(dist.items(), key= lambda x:x[1])[:10])
    else:
        dist = dict(sorted(dist.items(), key= lambda x:x[1]))
    
    return list(dist.keys())


def recommend_similar_wine(input_vec, doc, type):
    fields = {'_id':0, 'wine_id':1, 'kname':1, 'winery':1,'winetype':1, }
    if type =='all':
        id_list = find_similar_wine(input_vec,doc)
    elif type =='celler':
        id_list = find_similar_wine_celler(input_vec,doc)
    
    if len(id_list)==0:
        return 'There is not similar wine in wineceller'
    else:
        wine_list = db.wine_db.find({'wine_id':{'$in':id_list}},fields)
        return wine_list

#hashtag recommendation
def get_hashtag(id_list):
    fields = {'_id':0, 'wine_id':1, 'kr_country':1,'note_cat':1 }
    wine_data = list(db.recommend_db.find({'wine_id':{'$in':id_list}},fields))
    country = wine_data[3]['kr_country']
    notes = wine_data[3]['note_cat']
    
    note_dic = {"오크 숙성": [ '낯선', '미지의','모험적인','은은한', '숲속을 걷는 듯한', '중후한', '여운이 긴'],
    "붉은과일": ['설레는', '두근거리는', '기대되는', '상큼한', '사랑스러운', '풋풋한', '상큼한'],
    "흙/기타": ['이색적인', '잊지못할', '인생에 한번 쯤', '숲속을 걷는 듯한', '은은한'],
    "꽃" :[' 깨끗한', '몽환적인', '청량한', '싱그러운', '플로럴한', '정원을 걷는 듯한'],
    "열대과일" : ['안정적인', '편안한', '따뜻한'],
    "검은과일": ['성숙한', '고전적인', '야성적인', '귀족적인', '클래식한', '깊은 풍미의'],
    "나무과일": ['행복한', '풍요로운', '여유있는'], 
    "감귤류" : ['신나는', '발랄한', '즐거운'], 
    "향신료" : ['특별한', '특이한', '색다른'],
    "일반숙성": ['매혹적인', '이국적인', '진지한'],
    "채소/허브": ['새벽느낌의', '풋풋한', '싱그러운','생동감있는','신비로운','숲속을 걷는 듯한', '자연적인', '독특한']}
    
    country_dic=  {'A':['패셔너블한','섬세한','열정적인','친근한'],
             'B':['진취적인','강렬한','긍정적인','낙천적인'],
             'C':['도전적인','모험적인']}
    
    if country in ['프랑스,' '이탈리아']:
         country = random.choice(country_dic['A'])
    elif country in ['미국','스페인']:
        country = random.choice(country_dic['B']) 
    else: country = random.choice(country_dic['C'])
    
    notes_list=[]
    notes1= re.compile('[^ㄱ-ㅣ가-힣/+]').sub('', notes[0])
    notes2= re.compile('[^ㄱ-ㅣ가-힣/+]').sub('', notes[1])
    notes_list.append(random.choice(note_dic[notes1]))
    notes_list.append(random.choice(note_dic[notes2]))
    
    return country, notes_list

#food recommend
def get_foodmatchwine():
    food_dic = {
    '해산물': ['시푸드', '사시미', '해산물'],
    '이탈리아 요리': ['피자', '파스타',' 라자냐','토마토파스타','크림파스타'],
    '디저트':['케이크', '케잌','디저트'],
    '샤퀴테리':['하몽','살라미'],
    '소고기':['비프','스테이크','로스트비프'],
    '샐러드': ['과일','샐러드','열대과일'],
    '양고기':['양갈비','양고기'],
    '연성치즈':['연성치즈'],
    '경성치즈':['경성치즈', '반경성치즈'],
    '블루치즈':['블루치즈'],}
    
    foodtype= random.sample(list(food_dic.keys()),2)
    fields = {'_id':0, 'wine_id':1, 'kname':1, 'winery':1,'winetype':1, }
    
    wine_list1, wine_list2 = [], []
    wine_data1 = list(db.recommend_db.find({'food_list':{'$regex':random.choice(food_dic[foodtype[0]])}},{'_id':0, 'wine_id':1}).skip(3).limit(10))
    wine_data2 = list(db.recommend_db.find({'food_list':{'$regex':random.choice(food_dic[foodtype[1]])}},{'_id':0, 'wine_id':1}).skip(3).limit(10))
    for wine in wine_data1:
        wine_list1.append(wine['wine_id']) 
    for wine in wine_data2:
        wine_list2.append(wine['wine_id'])
    wine_list1 = list(db.wine_db.find({'wine_id':{'$in':wine_list1}},fields))
    wine_list2 = list(db.wine_db.find({'wine_id':{'$in':wine_list2}},fields))
    
    return foodtype, wine_list1, wine_list2

def get_foodscript(foodtype):
    if foodtype== '해산물':
            script= '사시미, 킹크랩, 씨푸드와 바다 느낌 가득한 와인은'
    elif foodtype == '이탈리아 요리':
            script='피자, 파스타, 라자냐, 다채로운 이탈리아 요리에 잘 어울리는 와인은'
    elif foodtype =='디저트':
            script='마카롱, 케이크, 달콤한 디저트와 가볍게 마실 와인은'
    elif foodtype =='샤퀴테리':
            script='짭짤하고 고소한 하몽, 살라미에 잘어울리는 와인은'
    elif foodtype == '소고기':
            script='잘 구운 스테이크와 와인으로 기분내고 싶은 날엔'
    elif foodtype == '양고기':
            script='부드러운 양갈비에 어울리는 와인은'
    elif foodtype == '샐러드':
            script='새콤달콤 과일과 아삭아삭 샐러드에 어울리는 와인은'
    elif foodtype == '연성치즈':
            script='고소한 크래커에 부드러운 까망베르! 촉촉한 치즈에 어울리는 와인'
    elif foodtype=='경성치즈':
            script='아작아작 독특한 식감과 밀도높은 풍미의 경성치즈에 어울리는 와인'
    elif foodtype=='블루치즈':
            script='톡 쏘는 블루치즈와 잘 어울리는 가벼운 와인'
    return script
            
    
        
    

    