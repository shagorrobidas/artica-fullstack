from django.views.generic import ListView
from apps.articles.models import Article
from .models import Category, SubCategory, SubSubCategory
from django.shortcuts import get_object_or_404

class CategoryArticleListView(ListView):
    template_name = 'categories/list.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        qs = Article.objects.filter(status='published')
        slug = self.kwargs.get('slug')
        sub_slug = self.kwargs.get('sub_slug')
        subsub_slug = self.kwargs.get('subsub_slug')

        if subsub_slug:
            self.category_obj = get_object_or_404(SubSubCategory, slug=subsub_slug, subcategory__slug=sub_slug, subcategory__category__slug=slug)
            qs = qs.filter(subsubcategory=self.category_obj)
        elif sub_slug:
            self.category_obj = get_object_or_404(SubCategory, slug=sub_slug, category__slug=slug)
            qs = qs.filter(subcategory=self.category_obj)
        else:
            self.category_obj = get_object_or_404(Category, slug=slug)
            qs = qs.filter(category=self.category_obj)
            
        return qs.select_related('category', 'subcategory', 'subsubcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category_obj
        if isinstance(self.category_obj, Category):
            context['subcategories'] = self.category_obj.subcategories.filter(is_active=True)
        elif isinstance(self.category_obj, SubCategory):
            context['subsubcategories'] = self.category_obj.subsubcategories.filter(is_active=True)
        return context
