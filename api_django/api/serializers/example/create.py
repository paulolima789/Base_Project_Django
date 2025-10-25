# api/serializers/example/create.py

from rest_framework import serializers
from api.models import Example

class ExampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('id', 'name', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O campo 'name' não pode ficar vazio.")
        return value

    def create(self, validated_data):
        # comportamento padrão do ModelSerializer já funciona, mantido para clareza
        return super().create(validated_data)