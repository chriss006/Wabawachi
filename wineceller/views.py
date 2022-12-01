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
        pk = request.GET.get('userid',None)
        
        #wine celler wine
        if not WineCeller.objects.filter(owner_id=pk).exists():
                        raise ModuleNotFoundError('WINECELLER DOES NOT EXISTS')
                
        wines =[]
        for wine in WineCeller.objects.filter(owner_id=pk):
                wines.append(wine.wine_id) 
                
        fields = {'_id':0, 'wine_id':1, 'wine_picture':1}
        wine_list =db.wine_db.find( {'wine_id':{'$in':wines}}, fields)
        
        return Response({'wine_celler': list(wine_list)})     

class RecentCollectedWineView(APIView):
    
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
        
        fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winetype':1}
        wine_list = db.wine_db.find( {'wine_id':{'$in':wines}}, fields)
        
        
        return Response(list(wine_list))
    
class WineCellerDetailView(APIView):
    def get(self, request, wine_id):
           
        #user auth
        access = request.COOKIES['access']
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
        pk = payload.get('user_id') 
        #review
        review = ReviewDetailSerialzier(Review.objects.get(wine_id=wine_id))
        #wine
        fields = {'_id':0, 'wine_id':1, 'kname':1, 'ename':1, 'winery':1, 'kr_country':1, 'kr_region':1, 'winetype':1}
        wine = db.wine_db.find_one( {'wine_id':wine_id}, fields)
        
        
        return Response({'wine_review': review.data, 'wine': wine})
        

class WineCellerTotalView(APIView):
    def get(self, request):
        #user auth
        access = request.COOKIES['access']
        payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])  
        pk = payload.get('user_id') 
        
        wines =[]
        for wine in WineCeller.objects.filter(owner_id=pk):
                wines.append(wine.wine_id)
        wine_list = db.wine_db.find({'wine_id':{'$in':wines}},{'_id':0,'wine_id':1, 'winetype':1})
        total = len(wines)
        red, white, other = 0,0,0,
        for wine in wine_list:
            if wine['winetype'] =='레드':
               red+=1
            elif wine['winetype'] =='화이트':
               white+=1
            else:
               other+=1
        return Response({'red':f'{red}/{total}', 'white':f'{white}/{total}','other':f'{other}/{total}'})
 