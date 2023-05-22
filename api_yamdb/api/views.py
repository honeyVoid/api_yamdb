from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status, serializers, viewsets, pagination, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import User

from .serializers import (TokenRequestSerializer, UserRegistrationSerializer,
                          UserSerializer, UserUpdateSerializer)


@api_view(['POST'])
def user_registration(request):
    '''
    Получает на вход username и email, после чего генерирует
    confirmation_code для последующей отправки на почту с целью
    генерации токена.
    '''
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    if username == 'me':
        raise serializers.ValidationError(
            "Использование 'me' в качестве username запрещено."
        )
    serializer.save()
    user = get_object_or_404(User, username=username)
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
            "username": str(user),
            "email": str(email)
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
        access = AccessToken.for_user(user)
        token = {
            'token': str(access)
        }
        return Response(token, status=status.HTTP_200_OK)
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
