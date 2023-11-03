from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title
from api.serializers import ReviewSerializer, CommentSerializer
from api.permission import IsAdminModeratorOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс для работы с отзывами."""
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
