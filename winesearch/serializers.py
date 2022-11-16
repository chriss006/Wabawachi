from rest_framework import serializers
from wineceller.models import Wine

class WineDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
       model = Wine
       fields ='__all__'
       

