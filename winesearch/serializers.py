from rest_framework import serializers
import json
from wineceller.models import Wine
from .models import Winesearch
class WineDetailSerializer(serializers.ModelSerializer):

    class Meta:
       model = Wine
       fields ='__all__'
       
class WineSearchSaveSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Winesearch
        fields = '__all__'

       

