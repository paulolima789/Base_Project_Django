# api/serializers/example/delete.py
from rest_framework import serializers
from api.models import Example

class ExampleDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'  # apenas para documentação, mas não será usado