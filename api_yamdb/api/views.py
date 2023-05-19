from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework import (
    viewsets, mixins
)

from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,

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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = (...)
    permission_classes = (...)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id']
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (...)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id']
        )
        serializer.save(author=self.request.user, review=review)
