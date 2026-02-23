"""
Views for API app.
"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import F
from .models import Article, Comment
from .serializers import (
    ArticleSerializer, ArticleListSerializer,
    CommentSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit their objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for the owner
        return obj.author == request.user


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Article CRUD operations.
    
    list: GET /api/articles/ - List all articles
    create: POST /api/articles/ - Create new article
    retrieve: GET /api/articles/{id}/ - Get article details
    update: PUT /api/articles/{id}/ - Update article
    destroy: DELETE /api/articles/{id}/ - Delete article
    """
    queryset = Article.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'views', 'published_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer

    def get_queryset(self):
        """Filter queryset based on user permissions."""
        queryset = super().get_queryset()
        
        # Non-authenticated users only see published articles
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        
        # Staff users see all articles
        if self.request.user.is_staff:
            queryset = Article.objects.all()
        
        return queryset

    def perform_create(self, serializer):
        """Set the author to the current user."""
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """Increment view count when article is retrieved."""
        instance = self.get_object()
        Article.objects.filter(pk=instance.pk).update(views=F('views') + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, slug=None):
        """Publish an article."""
        article = self.get_object()
        
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to publish this article.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        article.is_published = True
        article.published_at = timezone.now()
        article.save()
        
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unpublish(self, request, slug=None):
        """Unpublish an article."""
        article = self.get_object()
        
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'You do not have permission to unpublish this article.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        article.is_published = False
        article.save()
        
        serializer = self.get_serializer(article)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment CRUD operations.
    
    list: GET /api/comments/ - List all comments
    create: POST /api/comments/ - Create new comment
    retrieve: GET /api/comments/{id}/ - Get comment details
    update: PUT /api/comments/{id}/ - Update comment
    destroy: DELETE /api/comments/{id}/ - Delete comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter comments by article if provided."""
        queryset = super().get_queryset()
        article_slug = self.request.query_params.get('article')
        if article_slug:
            queryset = queryset.filter(article__slug=article_slug)
        return queryset

    def perform_create(self, serializer):
        """Set the author to the current user."""
        serializer.save(author=self.request.user)
