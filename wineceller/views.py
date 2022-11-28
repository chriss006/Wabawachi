from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wabawachi.settings import SECRET_KEY
from wineceller.models import WineCeller
from review.models import Review
from review.serializers import *
from pymongo import MongoClient
import jwt

client = MongoClient("mongodb://chriss:1234@3.38.2.131:27017")
db = client['winedb']

class WineCellerView(APIView):
    def get(self,request):
        #user auth
        access = request.COOKIES['access']
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
        pk = payload.get('user_id') 
        
        #wine celler wine
        if not WineCeller.objects.filter(owner_id=pk).exists():
                        raise ModuleNotFoundError('WINECELLER DOES NOT EXISTS')
                
        wines =[]
        for wine in WineCeller.objects.filter(owner_id=pk):
                wines.append(wine.wine_id) 
        
        return Response({'wine_celler': wines})        
            
class WineCellerDetailView(APIView):
    def get(self, request, wine_id):
           
        
        #user auth
        access = request.COOKIES['access']
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
        pk = payload.get('user_id') 
        #review
        review = ReviewDetailSerialzier(Review.objects.get(wine_id=wine_id))
        #wine
        fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, }
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)
        
        
        return Response({'wine_review': review.data, 'wine': wine})
        
    