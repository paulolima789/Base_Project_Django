# api/serializers/User/list.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # use USERNAME_FIELD (ex: 'email') e liste apenas campos existentes no seu model
        fields = (
            "id",
            USERNAME_FIELD,
            # adicione outros campos reais do model, ex:
            "name",
            "email",   # se duplicado com USERNAME_FIELD, mantenha só o necessário
            "is_active",
            "is_staff",
        )
        read_only_fields = ("id",)