from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404


from rest_framework import (status, viewsets,
                            pagination, permissions,
													  viewsets, mixins)


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


@api_view(['POST'])
def user_registration(request):
    '''
    Получает на вход username и email, после чего генерирует
    confirmation_code для последующей отправки на почту с целью
    генерации токена.
    '''
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    email = user.email
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения API YamDB',
        f'''
Вы зарегистрировались на YamDB под ником: {user}.
Ваш код подтверждения: {confirmation_code}''',
        'confirmation_code@yamdb.com',
        [email, ]
    )
    return Response(
        {
            'username': str(user),
            'email': str(email)
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes = (IsAdmin,)

    @action(['get', 'patch'],
            detail=False,
            url_path='me',
            permission_classes=(permissions.IsAuthenticated,),
            serializer_class=UserUpdateSerializer)
    def user_udate_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=200)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

