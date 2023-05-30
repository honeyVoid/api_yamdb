from django.conf import settings

from django.core.validators import MaxLengthValidator, RegexValidator
# from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)

RISTRICTED_SIMBOLS = r'^[\w.@+-]+\Z'
# спец-символы которые не должны быт в username


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id', )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id', )
        lookup_field = 'slug'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'genre', 'category', 'description'
        )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        required=False
    )
    author = serializers.SlugRelatedField(
        default=User,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, value):
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            title_id = self.context['view'].kwargs.get('title_id')
            if Review.objects.filter(
                author_id=user.id, title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Отзыв уже существует'
                )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=User,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(RISTRICTED_SIMBOLS)]
    )
    email = serializers.EmailField(max_length=254)

    def validate(self, attrs):
        email = User.objects.filter(
            email=attrs.get('email')
        ).exists()
        users = User.objects.filter(
            username=attrs.get('username')
        ).exists()
        if (email and not users):
            raise serializers.ValidationError(
                'This email is already registered.',
                code='email_registered'
            )
        if users and not email:
            raise serializers.ValidationError(
                'This username is already registered.',
                code='user_registered'
            )

        return attrs

    def validate_username(self, value):
        if value.lower() == settings.RISTRECTED_USERNAME:
            raise serializers.ValidationError(
                f'Username {settings.RISTRECTED_USERNAME} is not valid'
            )
        return value


class TokenRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio'
        )
        model = User


class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            MaxLengthValidator(150),
            RegexValidator(r'^[\w.@+-]+\Z')
        ]
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role', 'username')
        model = User
