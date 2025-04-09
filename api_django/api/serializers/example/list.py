# api/serializers/example/list.py

from rest_framework import serializers
from api.models import Example

class ExampleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'  # campos resumidos para listagem