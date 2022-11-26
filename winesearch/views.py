from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WineDetailSerializer,WineSearchSaveSerialzier
from elasticsearch import Elasticsearch
from pymongo import MongoClient
from users.models import User

client = MongoClient("3.38.57.203:27017")
db = client['winedb']


class SearchView(APIView):
    def get(self, request):
        es = Elasticsearch(['https://search-waba-cgvedgrfkpn7eoswsulfst47y4.ap-northeast-1.es.amazonaws.com'],
                           http_auth=('sesac', 'Winebasket1!'))

        origin_search = request.GET.get('search')

        if origin_search.encode().isalpha():
            # 영어일 때, 띄어쓰기 유지            
            search_word = origin_search
        else:
            # 한글일 때, 띄어쓰기 제거
            sl = list(origin_search.split())
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
                        "query": search_word
                    }
                    }
            }
        )
        data_list = []
        for data in docs['hits']['hits']:
            data_list.append(data.get('_source'))
        
        # 출력되는 데이터 없으면 data_list는 빈 리스트가 된다
        if len(data_list) == 0:
            docs = es.search(
                        index='wine_basket_search_engine',
                        body = {
                                "size": 50,
                                "query": {
                                "multi_match" : {
                                    "query": search_word,
                                    "fuzziness": "auto"
                                        }
                                    }
                                }
                            )
            for data in docs['hits']['hits']:
                data_list.append(data.get('_source'))
            

                    
        return Response(data_list)

      
    
class SearchDetailView(APIView):

    def get(self, request, wine_id):

        # 검색어
        fields = {'_id':0, 'wine_id':1,'wine_picture':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape_list':1, 'notes_list':1,'food_list':1 }
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)

    
        detail_serializer= WineDetailSerializer(data=wine)
        
        if detail_serializer.is_valid():  
            return Response({'wine_detail': wine})
        else:
            return Response(detail_serializer.errors)
        
    def post(self, request, wine_id):
        
        fields = {'_id':0, 'wine_id':1,'wine_picture':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'sweet':1, 'acidic':1, 'body':1, 'tannic':1 ,'winetype':1, 'kr_grape_list':1, 'notes_list':1,'food_list':1 }
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)
        
        data={}
        data['kname'] = wine['kname']
        data['wine_id'] = wine['wine_id']
        data['user'] =User.objects.get(username = request.data.get('username')).pk
        
        
        save_serializer = WineSearchSaveSerialzier(data=data)
        
        if save_serializer.is_valid():
            Wine = save_serializer.save()
            return Response(save_serializer.data)
        else:
            return Response(save_serializer.errors)
        
        
    
class AddWineCellerView(APIView):
    def post(self, request):

        detail_serializer = WineDetailSerializer(data=request.data)
        
        if detail_serializer.is_valid():
            Wine = detail_serializer.save()
            return Response(detail_serializer.data)
        else:
            return Response(detail_serializer.errors)
            
