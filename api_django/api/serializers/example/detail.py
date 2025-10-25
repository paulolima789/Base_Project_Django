# api/serializers/example/detail.py

from rest_framework import serializers
from api.models import Example

class ExampleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')