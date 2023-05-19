from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import (
    viewsets, mixins
)

from reviews.models import (
    Title,
    Genre,
    Category
)
from api.serializers import (
    GenreSerializer,
    TitleSerializer,
    CategorySerializer
)
from api.filters import TitleFilter


class CDULViewsSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    ...


class TitleVieSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (...)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class GenreViewSet(CDULViewsSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (...)
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = (...)


class CategoryViewSet(CDULViewsSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (...)
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = (...)
