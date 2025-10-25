# api/serializers/group/delete.py

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')