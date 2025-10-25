# api/serializers/example/list.py

from rest_framework import serializers
from api.models import Example

class ExampleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('id', 'name', 'created_at')  # campos resumidos para listagem
        read_only_fields = ('id', 'created_at')