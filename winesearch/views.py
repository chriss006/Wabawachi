from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WineDetailSerializer
from wineceller.models import Wine
from elasticsearch import Elasticsearch
import pymongo
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db = client['winedb']

class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'192.168.20.68', 'port':'9200'}])
        search_word_0 = request.GET.get('search')
        sl = list(search_word_0.split())
        search_word = ''.join(sl)
        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST,
            data={'message': 'search word param is missing'})
        docs = es.search(
            index='wine_basket',
            body = {
                  "query": {
                    "bool": {
                    "should": [{
                        "prefix": {
                        "kname": search_word
                        }
                    }, {
                        "term": {
                        "knameNgram": search_word
                        }
                    }, {
                        "term": {
                        "knameNgramEdge": search_word
                        }
                    }, {
                        "term": {
                        "knameNgramEdgeBack": search_word
                        }
                    }],
                    "minimum_should_match": 1
                    }
                }
            }
        )
        data_list = []
        for data in docs['hits']['hits']:
            data_list.append(data.get('_source'))
        return Response(data_list)
    
class SearchDetailView(APIView):

    def get(self, request, wine_id):

        # 검색어
        fields = {'_id':0, 'wine_id':1,'wine_picture':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape_list':1, 'notes_list':1,'food_list':1 }
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)

    
        detail_serializer= WineDetailSerializer(data=wine)
        
        # if detail_serializer.is_valid():  
        #     return Response({'wine_detail': wine})
        # else:
        #     return Response(detail_serializer.errors)
        return Response(wine)

        


class AddWineCellerView(APIView):
    def post(self, request):

        detail_serializer = WineDetailSerializer(data=request.data)
        
        if detail_serializer.is_valid():
            Wine = detail_serializer.save()
            return Response(detail_serializer.data)
        else:
            return Response(detail_serializer.errors)
            

 
    
    


    

