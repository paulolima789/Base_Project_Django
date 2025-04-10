# api/serializers/User/update.py

from rest_framework import serializers
from api.models import CustomUser

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  # apenas os campos que podem ser atualizados
