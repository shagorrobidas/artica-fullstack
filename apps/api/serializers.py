from rest_framework import serializers
from apps.categories.models import Category, SubCategory
from apps.articles.models import Article, ArticleSection, Tag
from apps.media_manager.models import ArticleMedia
from apps.glossary.models import InteractiveTerm





class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [
            'id',
            'name',
            'slug',
            'description'
        ]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'subcategories'
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'slug'
        ]


class ArticleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSection
        fields = [
            'id',
            'title',
            'content',
            'order',
            'is_expanded_default'
        ]


class ArticleMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleMedia
        fields = [
            'id',
            'label',
            'text_content',
            'image',
            'audio_file',
            'video_file',
            'youtube_url',
            'order'
        ]


class InteractiveTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractiveTerm
        fields = [
            'id',
            'term',
            'slug',
            'explanation',
            'image',
            'audio_file',
            'external_link'
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'subtitle',
            'slug',
            'author',
            'category_name',
            'cover_image',
            'excerpt',
            'published_at',
            'view_count',
            'tags'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    sections = ArticleSectionSerializer(many=True, read_only=True)
    media = ArticleMediaSerializer(many=True, read_only=True)
    # Custom field to load terms
    terms = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'subtitle',
            'slug',
            'author',
            'cover_image',
            'body',
            'excerpt',
            'published_at',
            'view_count',
            'tags',
            'sections',
            'media',
            'terms',
            'category',
            'subcategory'
        ]

    def get_terms(self, obj):
        mappings = obj.term_mappings.select_related('term')
        return [InteractiveTermSerializer(m.term).data for m in mappings]
