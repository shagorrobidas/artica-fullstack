from django.contrib import admin
from .models import InteractiveTerm, ArticleTermMapping

@admin.register(InteractiveTerm)
class InteractiveTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'slug', 'created_at')
    search_fields = ('term', 'explanation')
    prepopulated_fields = {'slug': ('term',)}

@admin.register(ArticleTermMapping)
class ArticleTermMappingAdmin(admin.ModelAdmin):
    list_display = ('term', 'article', 'occurrence_index')
    search_fields = ('term__term', 'article__title')
    list_filter = ('term',)
    raw_id_fields = ('article', 'term')
