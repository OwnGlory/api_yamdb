from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet
)

router = DefaultRouter()

router.register('categories', CategoryViewSet, basename='categoies')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register((r'titles/(?P<title_id>\d+)/reviews/'
                r'(?P<review_id>\d+)/comments'),
                CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]
