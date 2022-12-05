from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wabawachi.settings import SECRET_KEY
from .recommend import *
from .trending import trending_list
from review.models import Review
from winesearch.models import Winesearch
from wineceller.models import WineCeller
from pymongo import MongoClient
import jwt


client = MongoClient("mongodb://chriss:1234@3.38.2.131:27017")
db = client['winedb']

class SimilarWineAllListView(APIView):
        def post(self, request):
                
                pk = request.data.get('user_id')
                
                wine_id = Winesearch.objects.filter(user_id=pk)[0].wine_id
    
                doc = preprocess_doc()
                input_vec = doc[doc['wine_id']==wine_id].values
                wine_list= recommend_similar_wine(input_vec, doc, type='all')
                
                return Response(list(wine_list))

class SimilarWineCellerListView(APIView):
        def post(self, request):
                
                #user
                pk = request.data.get('user_id')
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
        
class HashtagRecommendListView(APIView):
        def post(self, request):
                
                #user
                pk = request.data.get('user_id')
                
                if not Review.objects.filter(user_id=pk).exists():
                        raise ModuleNotFoundError('WINECELLER DOES NOT EXISTS')
                
                wines =[]
                for wine in Review.objects.filter(user_id=pk, assessment='좋음'):
                        wines.append(wine.wine_id)                        
 
                wine_id, wines = hashtag_similar_wine(pk)
                country, notes = get_hashtag_script(wine_id)
                return Response({'script': f'#{country}, #{notes[0]} 와인을 좋아하는 당신에게',
                                 'wine_list' :wines,})
                
                
class TrendingWineListView(APIView):
        def get(self, request):
                wine_list = trending_list()
                
                fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winetype':1, 'wine_picture':1}
                trending_wines = db.wine_db.find( {'wine_id':{'$in':wine_list}}, fields)
                return Response(list(trending_wines))
        

class FoodMatchWineListView(APIView):
        def get(self, request):
                foodtype, wine_list1, wine_list2, wine_list3, wine_list4 = get_foodmatchwine()
                script1 = get_foodscript(foodtype[0])
                script2 = get_foodscript(foodtype[1])
                script3 = get_foodscript(foodtype[3])
                script4 = get_foodscript(foodtype[4])

                return Response({'foodscript1':script1, 'wine_list1':wine_list1,'foodscript2':script2, 'wine_list2':wine_list2, 'foodscript3':script3, 'wine_list3':wine_list3 ,'foodscript4':script4, 'wine_list4':wine_list4 })

                
        