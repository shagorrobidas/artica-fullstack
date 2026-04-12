from django.views.generic import ListView
from apps.articles.models import Article
from django.db.models import Q


class SearchResultsView(ListView):
    model = Article
    template_name = 'search/results.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Article.objects.filter(
                Q(
                    title__icontains=query
                ) | Q(
                    excerpt__icontains=query
                ) | Q(
                    body__icontains=query
                ),
                status='published'
            ).select_related('category')
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
