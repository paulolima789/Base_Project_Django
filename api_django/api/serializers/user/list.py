# api/serializers/User/list.py

from rest_framework import serializers
from api.models import CustomUser

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # campos resumidos para listagem