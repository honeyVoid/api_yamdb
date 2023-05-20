from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import token_request, UserRegistrationViewSet



router = DefaultRouter()
# router.register('user', UserViewSet)
router.register('signup', UserRegistrationViewSet)

urlpatterns = [
    path('v1/auth/', include(router.urls)),
    path('v1/auth/token/', token_request)
]


# Самостоятельная регистрация новых пользователей
# Пользователь отправляет POST-запрос с параметрами email и 
# username на эндпоинт /api/v1/auth/signup/.
# Сервис YaMDB отправляет письмо с кодом подтверждения 
# (confirmation_code) на указанный адрес email.
# Пользователь отправляет POST-запрос с параметрами username и 
# confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на 
# запрос ему приходит token (JWT-токен).
# В результате пользователь получает токен и может работать с API 
# проекта, отправляя этот токен с каждым запросом. 
# После регистрации и получения токена пользователь может отправить 
# PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в 
# своём профайле (описание полей — в документации).

# Создание пользователя администратором
# Пользователей создаёт администратор — через админ-зону сайта или 
# через POST-запрос на специальный эндпоинт api/v1/users/ 
# (описание полей запроса для этого случая есть в документации). 
# При создании пользователя не предполагается автоматическая 
# отправка письма пользователю с кодом подтверждения. 
# После этого пользователь должен самостоятельно отправить свой 
# email и username на эндпоинт /api/v1/auth/signup/ , в ответ ему 
# должно прийти письмо с кодом подтверждения.
# Далее пользователь отправляет POST-запрос с параметрами username 
# и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на 
# запрос ему приходит token (JWT-токен), как и при самостоятельной 
# регистрации.