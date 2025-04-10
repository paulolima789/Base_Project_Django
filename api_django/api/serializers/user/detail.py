# api/serializers/User/detail.py

from rest_framework import serializers
from api.models import CustomUser

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # ou lista de campos completa