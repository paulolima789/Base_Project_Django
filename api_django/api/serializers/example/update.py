# api/serializers/example/update.py

from rest_framework import serializers
from api.models import Example

class ExampleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ('id', 'name', 'description', 'updated_at')
        read_only_fields = ('id', 'updated_at')

    def validate_name(self, value):
        if value is not None and not value.strip():
            raise serializers.ValidationError("O campo 'name' não pode ficar vazio.")
        return value

    def update(self, instance, validated_data):
        # atualiza apenas os campos permitidos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
