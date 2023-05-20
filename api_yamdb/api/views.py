from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import viewsets, mixins, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken



from reviews.models import User

from .serializers import TokenRequestSerializer, UserRegistrationSerializer

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserRegistrationViewSet(mixins.CreateModelMixin, 
                              viewsets.GenericViewSet):
    '''
    Получает на вход username и email, после чего генерирует 
    confirmation_code для последующей отправки на почту с целью
    генерации токена.
    '''
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def send_confirmation_code(self, username, email, confirmation_code):
        send_mail(
            'Код подтверждения API YamDB', 
            f'''
Вы зарегистрировались на YamDB под ником: {username}.
Ваш код подтверждения: {confirmation_code}''', 
            'confirmation_code@yamdb.com', 
            [email]
        )

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if username == 'me':
            raise serializers.ValidationError(
                "Использование 'me' в качестве username запрещено."
            )
        code = get_random_string(length=32)
        serializer.save(confirmation_code=code)
        self.send_confirmation_code(
            serializer.validated_data.get('username'),
            serializer.validated_data.get('email'), 
            code,
        )


@api_view(['POST'])
def token_request(request):
    serializer = TokenRequestSerializer(data=request.data)
    if serializer.is_valid():
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = User.objects.get(username=username)
        try:
            if user.confirmation_code == confirmation_code:
                access = AccessToken.for_user(user)
                token = {
                    'token': str(access)
                }
                return Response(token, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'Ошибка': 'Неверный код подтверждения '}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'Ошибка': 'Пользователь не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )
 