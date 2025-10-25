# api/serializers/User/detail.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # campos existentes no model User
        fields = ('id', USERNAME_FIELD, 'name', 'is_active', 'is_staff')