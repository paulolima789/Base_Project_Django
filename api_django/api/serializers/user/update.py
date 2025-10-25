# api/serializers/User/update.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
USERNAME_FIELD = User.USERNAME_FIELD

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        # adapte os campos que podem ser atualizados; incluir password como write_only
        fields = ('id', USERNAME_FIELD, 'name', 'is_active', 'is_staff', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
