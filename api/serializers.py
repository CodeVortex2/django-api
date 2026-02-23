"""
Serializers for API app.
"""
from rest_framework import serializers
from .models import Article, Comment
from accounts.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'author_email', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for Article model."""
    author_details = UserSerializer(source='author', read_only=True)
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'author', 'author_details',
            'image', 'is_published', 'views', 'comments_count', 'comments',
            'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = ['id', 'author', 'views', 'created_at', 'updated_at', 'published_at']

    def get_comments_count(self, obj):
        """Return the number of comments for this article."""
        return obj.comments.count()


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for Article list view (simplified)."""
    author_email = serializers.ReadOnlyField(source='author.email')
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'author_email', 'image',
            'is_published', 'views', 'comments_count', 'created_at'
        ]

    def get_comments_count(self, obj):
        """Return the number of comments for this article."""
        return obj.comments.count()
