
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    TitleVieSet,
		token_request,
		user_registration
)
router = DefaultRouter()
router.register(r'titles', TitleVieSet)
urlpatterns = [
    path('v1/', include(router.urls)),
		path('v1/auth/signup/', user_registration),
    path('v1/auth/token/', token_request)
]
