from elasticsearch import Elasticsearch
from math import sqrt
es = Elasticsearch([{'host':'3.38.2.131', 'port':'9200'}])

score_dict = {}

docs = es.search(
    index='wabawachi_logs',
    body = {
        "size": 0,
        # 조건문
        "query": {
            "bool": {
                "must": [{
                    "wildcard": {
                        "request_url": {
                            "value": "/api/v1/winesearch/detail/*"
                    }}},
                    {"range": {
                        "@timestamp": {
                            "gte": "now-1M",
                            "lte": "now"
                    }}},
                    {"match": {
                        "method": "POST"
                    }}]
                }
        },  
        # 집계함수
        "aggs": {
            "histogram_aggs": {
            "date_histogram": {
                "field": "@timestamp",
                "interval": "hour"
            },
            "aggs": {
            "by_request_url": {
                "terms": {
                "field": "request_url"
                }
            }
            }
        }
        }
    }
)

value = 1
for datas in docs['aggregations']['histogram_aggs']['buckets']:
    for data in datas['by_request_url']['buckets']:    
        a = data.get('key')
        b = data.get('doc_count')
        if a in score_dict: score_dict[a] += (b*sqrt(value))
        else: score_dict[a] = (b*sqrt(value))
    value += 1

# print(score_dict)

sorted_score_dict = sorted(score_dict.items(), key = lambda item: item[1], reverse= True)
# print('-------------------------------')
print(sorted_score_dict[:10])