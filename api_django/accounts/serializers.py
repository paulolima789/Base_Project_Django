from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import SocialAccount

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_social_account')

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'
