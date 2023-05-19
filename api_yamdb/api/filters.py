from django_filters import rest_framework

from reviews.models import (
    Title,
)


class TitleFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        lookup_expr='icontains'
    )
    genre = rest_framework.CharFilter(
        lookup_expr='icontains'
    )
    category = rest_framework.CharFilter(
        lookup_expr='icontains'
    )
    year = rest_framework.CharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'genre',
            'category',
            'year'
        )
