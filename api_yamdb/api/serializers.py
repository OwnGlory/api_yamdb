from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title',),
                message="Нельзя оставить отзыв второй раз."
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моедлью Comment."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
