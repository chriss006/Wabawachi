import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pymongo
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db = client['winedb']


# 추천시스템
docs = db.wine_db.find({},{'_id':0, 'wine_id':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape':1})

doc = pd.DataFrame(docs, columns=['wine_id','sweet','acidic','body','tannic','winetype','kr_grape'])

def preprocess(doc):
    le = LabelEncoder()
    doc['kr_grape'] = le.fit_transform(doc['kr_grape'])
    doc['winetype'] = le.fit_transform(doc['winetype']) 
    return doc

def find_similar_wine(input_vec, doc):
    dist={}

    for i in doc['wine_id']:
        if input_vec[0][0]!=i: 
            temp = doc.loc[i,['sweet','acidic','body','tannic','winetype','kr_grape']]
            dist[i]=np.sum(np.square(input_vec[0][1:] - temp.to_numpy()))

    dist = dict(sorted(dist.items(), key= lambda x:x[1])[:5])
    
    return list(dist.keys())

def recommend_similar_wine(input_vec, doc):
    
    fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape_list':1, 'note_list':1,'food_list':1 }
    id_list = find_similar_wine(input_vec,doc)
    wine_list = db.wine_db.find({'wine_id':{'$in':id_list}},fields)
    return wine_list