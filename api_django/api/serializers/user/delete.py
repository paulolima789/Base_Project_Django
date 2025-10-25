# api/serializers/User/delete.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # só para documentação / resposta; não inclui password
        fields = ('id', USERNAME_FIELD, 'name')