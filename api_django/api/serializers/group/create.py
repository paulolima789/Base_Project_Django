# api/serializers/group/create.py

from rest_framework import serializers
from django.contrib.auth.models import Group, Permission

class GroupCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')

    def create(self, validated_data):
        perms = validated_data.pop('permissions', [])
        group = Group.objects.create(**validated_data)
        if perms:
            group.permissions.set(perms)
        return group