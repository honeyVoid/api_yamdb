from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from reviews. models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,
)


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
            'id', 'name', 'year', 'rating', 'genre', 'category'
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


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'username')
        model = User


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

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)
        model = User
