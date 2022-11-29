import numpy as np
import pandas as pd
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
def get_attributes_hash(id_list):
    fields = {'_id':0, 'wine_id':1, 'kr_country':1,'note_cat':1 }
    wine_data = list(db.recommend_db.find({'wine_id':{'$in':id_list}},fields))
    return wine_data
    