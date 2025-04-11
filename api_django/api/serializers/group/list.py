# api/serializers/group/list.py

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'