# api/serializers/User/delete.py
from rest_framework import serializers
from api.models import CustomUser

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # apenas para documentação, mas não será usado