from rest_framework import serializers

from reviews.models import User



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = '__all__'
#         model = User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User


# class TokenRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('username', 'confirmation_code')
#         model = User
        
class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()