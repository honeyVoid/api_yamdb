from rest_framework import serializers

from reviews. models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User,  # заплатка до создания серилазатора User
)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        model = Title
        exclude = ('pk', )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('pk', )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('pk', )


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
        read_only_fields = ('review', )
