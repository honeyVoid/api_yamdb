from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    TitleVieSet
)
router = DefaultRouter()
router.register(r'titles', TitleVieSet)
urlpatterns = [
    path('v1/', include(router.urls))
]
