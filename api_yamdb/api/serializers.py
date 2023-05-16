from rest_framework import serializers

from reviews. models import (
    Title,
    Category,
    Genre
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
