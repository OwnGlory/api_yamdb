from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters import rest_framework as fs

from reviews.models import (Review, Title, Category, Genre, Title)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReadOnlyTitleSerializer,
    CommentSerializer,
    ReviewSerializer
)
from users.permissions import (IsAdminModeratorOwnerOrReadOnly,
                               IsAdminOrReadOnly)


class TitleFilter(fs.FilterSet):
    name = fs.CharFilter(field_name='name')
    category = fs.CharFilter(field_name='category', lookup_expr='slug')
    genre = fs.CharFilter(field_name='genre', lookup_expr='slug')
    year = fs.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    filter_backends = (fs.DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы с отзывами."""
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=get_object_or_404(
                Title, pk=self.kwargs.get('title_id')
            ), author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Класс для работы с комментариями."""
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=get_object_or_404(Review, pk=self.kwargs.get('review_id')),
            author=self.request.user
        )
