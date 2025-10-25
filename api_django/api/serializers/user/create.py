# api/serializers/user/create.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # use USERNAME_FIELD (ex: 'email') e campos reais do model (name, is_active, is_staff)
        fields = ('id', USERNAME_FIELD, 'name', 'password', 'is_active', 'is_staff')
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        # use create_user para garantir hashing da senha e comportamento correto do user model
        user = User.objects.create_user(**validated_data, password=password)
        return user