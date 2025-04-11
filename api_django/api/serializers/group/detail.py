# api/serializers/group/detail.py

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'