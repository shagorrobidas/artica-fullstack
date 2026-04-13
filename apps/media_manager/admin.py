from django.contrib import admin
from .models import ArticleMedia

@admin.register(ArticleMedia)
class ArticleMediaAdmin(admin.ModelAdmin):
    list_display = ('article', 'label', 'order')
    search_fields = ('label', 'article__title')
    list_editable = ('order',)
