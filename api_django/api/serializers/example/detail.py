# api/serializers/example/detail.py

from rest_framework import serializers
from api.models import Example

class ExampleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'  # ou lista de campos completa