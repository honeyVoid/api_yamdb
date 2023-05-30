from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
    token_request,
    user_registration
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')
router.register(r"users", UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', user_registration),
    path('v1/auth/token/', token_request)
]
