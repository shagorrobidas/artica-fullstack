from django.contrib import admin
from .models import Article, Tag, ArticleSection
from apps.media_manager.models import ArticleMedia
from apps.glossary.models import ArticleTermMapping

class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1

class ArticleMediaInline(admin.StackedInline):
    model = ArticleMedia
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('media_type', 'label', 'order')
        }),
        ('Content (Fill based on media_type)', {
            'fields': ('text_content', 'image', 'audio_file', 'video_file', 'youtube_url'),
            'classes': ('collapse',),
            'description': ("Only fill the field that matches the chosen 'media_type'.")
        }),
    )

class ArticleTermMappingInline(admin.TabularInline):
    model = ArticleTermMapping
    extra = 1
    raw_id_fields = ('term',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'is_featured', 'published_at', 'view_count')
    list_filter = ('status', 'is_featured', 'category')
    search_fields = ('title', 'subtitle', 'body')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleSectionInline, ArticleMediaInline, ArticleTermMappingInline]
    filter_horizontal = ('tags',)
    readonly_fields = ('view_count',)
    fieldsets = (
        ('General', {
            'fields': ('title', 'subtitle', 'slug', 'author', 'status', 'is_featured')
        }),
        ('Hierarchy', {
            'fields': ('category', 'subcategory', 'subsubcategory')
        }),
        ('Content', {
            'fields': ('cover_image', 'excerpt', 'body', 'tags')
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description', 'published_at', 'view_count'),
            'classes': ('collapse',)
        }),
    )
