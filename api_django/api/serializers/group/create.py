# api/serializers/group/create.py

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'