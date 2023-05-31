from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import (status, viewsets,
                            pagination, permissions,
                            viewsets, mixins,
                            filters,)
from django_filters.rest_framework import DjangoFilterBackend


from api.permissions import (
    IsAdmin,
    IsAdminModeratorOwnerOrReadOnly,
    IsAdminOrReadOnly
)
from reviews.models import (
    Category,
    Genre,
    Review,
    Title,
    User,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenRequestSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ReadOnlyTitleSerializer

)
from api.filters import TitleFilter


class CustomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


@api_view(('POST',))
def user_registration(request):
    '''
    Получает на вход username и email, после чего генерирует
    confirmation_code для последующей отправки на почту с целью
    генерации токена.
    '''
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.validated_data.get('username'),
        email=serializer.validated_data.get('email')
    )
    email = user.email
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        settings.MAIL_THEME,
        f'''
{settings.ABOUT_REGISTRATION_MESSAGE}{user}.
{settings.CONFIRMATION_CODE_MESSAGE}{confirmation_code}''',
        f'{settings.EMAIL_SEND_FROM}',
        [email, ]
    )
    return Response(
        {
            'username': str(user),
            'email': str(email)
        },
        status=status.HTTP_200_OK
    )


@api_view(('POST',))
def token_request(request):
    serializer = TokenRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        return Response(
            {'Token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK
        )
    return Response(
        {'Ошибка': 'Неверный код подтверждения '},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = (IsAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)

    @action(('get', 'patch'),
            detail=False,
            url_path='me',
            permission_classes=(permissions.IsAuthenticated,),
            serializer_class=UserUpdateSerializer)
    def user_udate_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
