from django.contrib import admin
from .models import ArticleMedia

@admin.register(ArticleMedia)
class ArticleMediaAdmin(admin.ModelAdmin):
    list_display = ('article', 'media_type', 'label', 'order')
    list_filter = ('media_type',)
    search_fields = ('label', 'article__title')
    list_editable = ('order',)
