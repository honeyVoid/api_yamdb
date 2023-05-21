from rest_framework import serializers

from reviews.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
