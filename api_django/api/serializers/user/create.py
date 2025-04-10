# api/serializers/user/create.py

from rest_framework import serializers
from api.models import CustomUser

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # adapte os campos