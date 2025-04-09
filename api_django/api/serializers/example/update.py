# api/serializers/example/update.py

from rest_framework import serializers
from api.models import Example

class ExampleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = '__all__'  # apenas os campos que podem ser atualizados
