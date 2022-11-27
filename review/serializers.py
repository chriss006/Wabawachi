from rest_framework import serializers
import json
from .models import Review

class ReviewSaveSerialzier(serializers.ModelSerializer):
    
    
    class Meta:
        model = Review
        fields = '__all__'
