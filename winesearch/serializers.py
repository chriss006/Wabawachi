from rest_framework import serializers
import json
from .models import Winesearch
class WineDetailSerializer(serializers.Serializer):

    wine_id = serializers.IntegerField()
    wine_picture = serializers.URLField()
    kname = serializers.CharField( max_length=100)
    ename = serializers.CharField( max_length=100)
    winetype = serializers.CharField( max_length=10)
    kr_country =serializers.CharField( max_length=50)
    kr_region = serializers.CharField( max_length=50)
    kr_grape_list = serializers.ListField(child=serializers.CharField(max_length=20))  
    sweet = serializers.IntegerField()
    acidic= serializers.IntegerField()
    body = serializers.IntegerField()
    tannic = serializers.IntegerField()
    notes_list =serializers.ListField(child=serializers.CharField(max_length=20) )  
    food_list = serializers.ListField(child=serializers.CharField(max_length=20))  

class WineSearchSaveSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Winesearch
        fields = '__all__'

       

