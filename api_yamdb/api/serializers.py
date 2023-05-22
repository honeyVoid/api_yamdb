from rest_framework import serializers

from reviews.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'username')
        model = User


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        ),
        required=True,
    )
    email = serializers.EmailField(
        validators=(
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        fields = (
            'username',
            'email',
            'role',
        )
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
