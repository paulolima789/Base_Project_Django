# api/serializers/example/delete.py
from rest_framework import serializers
from api.models import Example

class ExampleDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('id', 'name')  # apenas para resposta/documentação
        read_only_fields = ('id',)