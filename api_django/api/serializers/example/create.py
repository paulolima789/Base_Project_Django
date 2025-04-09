# api/serializers/example/create.py

from rest_framework import serializers
from api.models import Example

class ExampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'  # adapte os campos