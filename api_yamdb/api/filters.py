from django_filters import rest_framework

from reviews.models import (
    Title,
)


class TitleFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        lookup_expr='icontains',
        field_name='name'
    )
    genre = rest_framework.CharFilter(
        lookup_expr='icontains',
        field_name='genre__slug'
    )
    category = rest_framework.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    year = rest_framework.CharFilter(
        lookup_expr='icontains',
        field_name='year'
    )
    description = rest_framework.CharFilter(
        lookup_expr='icontains',
        field_name='description'
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'genre',
            'category',
            'year',
            'description',
        )
