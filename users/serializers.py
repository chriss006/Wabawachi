from .models import User
from rest_framework import serializers

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data['password'],
            gender = validated_data['gender'],
            region = validated_data['region'],
            birthdate =validated_data['birthdate'],
        )
        return user


        