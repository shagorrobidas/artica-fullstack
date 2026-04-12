from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.categories.models import Category
from apps.articles.models import Article
from apps.glossary.models import InteractiveTerm
from .serializers import (
    CategorySerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    InteractiveTermSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(
        is_active=True
    ).prefetch_related('subcategories')
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['category__slug', 'tags__slug']
    search_fields = ['title', 'body', 'excerpt']
    ordering_fields = ['published_at', 'view_count']
    lookup_field = 'slug'

    def get_queryset(self):
        qs = Article.objects.filter(status='published')
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                'sections',
                'media',
                'term_mappings__term',
                'tags'
            ).select_related(
                'category',
                'subcategory'
            )
        else:
            qs = qs.select_related('category').prefetch_related('tags')
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer


class InteractiveTermViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InteractiveTerm.objects.all()
    serializer_class = InteractiveTermSerializer
    lookup_field = 'slug'
