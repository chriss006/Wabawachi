from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from wabawachi.settings import SECRET_KEY
from .serializers import WineDetailSerializer,WineSearchSaveSerialzier
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from wineceller.models import WineCeller
from winesearch.models import Winesearch
from review.models import Review
import jwt

client = MongoClient("mongodb://chriss:1234@3.38.2.131:27017")
db = client['winedb']


class SearchView(APIView):

    def get(self, request):
        es = Elasticsearch([{'host':'localhost', 'port':'9200'}])
        search_word_0 = request.GET.get('search')
        if search_word_0.encode().isalpha():
            search_word = search_word_0
        else:
            sl = list(search_word_0.split())
            search_word = ''.join(sl)

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST,
            data={'message': 'search word param is missing'})

        docs = es.search(
            index='wine_basket_search_engine',
            body = {
                "size": 50,
                  "query": {
                    "multi_match" : {
                        "query": search_word,
                        "fuzziness": "auto",
                        "fields": ["ename", "kname", "knameNgram", 
                        "knameNgramEdge", "knameNgramEdgeBack", "kr_concat"]
                    }
                  }
            }
        )

        data_list = []
        for data in docs['hits']['hits']:
            data_list.append(data.get('_source'))
        
        # 출력되는 데이터 없으면 data_list는 빈 리스트가 된다
        
        if len(data_list) == 0:
            # 영한 변환 검색 실시
            docs_ek = es.search(
                index='wine_basket_search_engine',
                body = {
                    "size": 5,
                        "query": {
                            "multi_match" : {
                                "query": search_word,
                                "analyzer": "eng2kor_analyzer"
                            }
                        }
                    }
                )
            # 한영 변환 검색 실시
            docs_ke = es.search(
                index='wine_basket_search_engine',
                body = {
                    "size": 5,
                        "query": {
                            "multi_match" : {
                                "query": search_word,
                                "analyzer": "kor2eng_analyzer"
                            }
                        }
                    }
                )
            # 초성 변환 검색 실시
            docs_chosung = es.search(
                index='wine_basket_search_engine',
                body = {
                    "size": 5,
                        "query": {
                            "match" : {
                                "knameChosung": {
                                    "query": search_word
                                }
                            }
                        }
                    }
                )

            for data in docs_ek['hits']['hits']:
                data_list.append(data.get('_source'))
            for data in docs_ke['hits']['hits']:
                data_list.append(data.get('_source'))
            for data in docs_chosung['hits']['hits']:
                data_list.append(data.get('_source'))

        return Response(data_list[:5])
    
    

      
    
class SearchDetailView(APIView):
    
    def post(self, request, wine_id):
        
        fields = {'_id':0, 'wine_id':1,'wine_picture':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape_list':1, 'notes_list':1,'food_list':1 }
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)

        pk = request.data.get('user_id')
        data={}
        data['kname'] = wine['kname']
        data['wine_id'] = wine['wine_id']
        data['user'] = pk

        save_serializer = WineSearchSaveSerialzier(data=data)
        detail_serializer= WineDetailSerializer(data=wine)
        
        if save_serializer.is_valid():
            save_serializer.save()
            print(save_serializer.data)
        else:
            return Response(save_serializer.errors)
            
        if detail_serializer.is_valid() :
            return Response({'wine_detail':detail_serializer.data})
        else:
            return Response(detail_serializer.errors)
        

        
class RecentSearchedWineView(APIView):
    def post(self, request):
                
        user = request.data.get('user_id')  
        
        if not Winesearch.objects.get(user_id=user).exists():
            return Response('최근 검색한 와인이 없습니다.')
        
        wines = Winesearch.objects.get(user_id=user)
        wine_id=[]
        for wine in wines:
            wine_id.append(wine.wine_id)
        fields = {'_id':0, 'wine_id':1, 'kname':1, 'winery':1, 'winetype':1, 'wine_picture':1}
        wine_list = list(db.wine_db.find( {'wine_id':{'$in':wine_id}}, fields))
        
        return Response(wine_list)

class AddWineCellerView(APIView):
    
    def post(self, request, wine_id):
        
        try:
            request.POST._mutable = True
            #user
            owner = request.data.get('user_id')  
            #wineceller
            total = WineCeller.objects.count()
            print(total)
            if WineCeller.objects.filter( owner_id=owner, wine_id=wine_id).exists():
                return Response('Wine Alread Exists')
            else:
                WineCeller.objects.create(id=total+1, owner_id=owner, wine_id=wine_id).save()
            
            #Review
            assessment = request.data.get('assessment')
            date = request.data.get('date')
            hashtag = request.data.get('hashtag')
            review = Review.objects.create(id=total+1, user_id=owner, wine_id=wine_id, assessment=assessment, date=date, hashtag=hashtag)
            review.save()
            return Response({'message':'WINE_ADDED'})

        except KeyError: 
            return Response({"message": "KEY_ERROR"}, status=400)
            

 
    
    


    

