from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wabawachi.settings import SECRET_KEY
from .recommend import *
from .trending import trending_list
from winesearch.models import Winesearch
from wineceller.models import WineCeller
from pymongo import MongoClient
import jwt


client = MongoClient("mongodb://chriss:1234@3.38.2.131:27017")
db = client['winedb']

class SimilarWineAllListView(APIView):
        def get(self, request):
                
                access = request.COOKIES['access']
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
                pk = payload.get('user_id') 
                
                wine_id = Winesearch.objects.filter(user_id=pk)[0].wine_id
    
                doc = preprocess_doc()
                input_vec = doc[doc['wine_id']==wine_id].values
                wine_list= recommend_similar_wine(input_vec, doc, type='all')
                
                return Response(list(wine_list))

class SimilarWineCellerListView(APIView):
        def get(self, request):
                
                #user
                access = request.COOKIES['access']
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
                pk = payload.get('user_id') 
                #wine_id
                wine_id = Winesearch.objects.filter(user_id=pk)[0].wine_id
                
                if not WineCeller.objects.filter(owner_id=pk).exists():
                        raise ModuleNotFoundError('WINECELLER DOES NOT EXISTS')
                
                wines =[]
                for wine in WineCeller.objects.filter(owner_id=pk):
                        wines.append(wine.wine_id)                        
                
                input_vec, docs = get_attributes(wine_id, wines)
                wine_list= recommend_similar_wine(input_vec, docs, type='celler')
                
                return Response(list(wine_list))
                
                
class TrendingWineListView(APIView):
        def get(self, request):
                wine_list = trending_list()
                
                fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winetype':1}
                trending_wines = db.wine_db.find( {'wine_id':{'$in':wine_list}}, fields)
                return Response(list(trending_wines))