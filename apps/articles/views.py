from django.views.generic import ListView, DetailView
from django.db import models
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 12

    def get_queryset(self):
        qs = Article.objects.filter(
            status='published'
        ).select_related('category', 'subcategory')
        tag = self.request.GET.get('tag')
        if tag:
            qs = qs.filter(tags__slug=tag)
        return qs


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related(
            'category', 'subcategory'
        ).prefetch_related(
            'sections',
            'media',
            'term_mappings__term',
            'tags'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Increment view count
        Article.objects.filter(
            pk=self.object.pk
        ).update(view_count=models.F('view_count') + 1)
        self.object.view_count += 1

        # Related articles (same category)
        if self.object.category:
            context['related_articles'] = Article.objects.filter(
                status='published', category=self.object.category
            ).exclude(pk=self.object.pk).order_by('-published_at')[:3]

        # Prepare terms data for frontend JS
        terms_data = {}
        for mapping in self.object.term_mappings.all():
            term = mapping.term
            terms_data[term.slug] = {
                'term': term.term,
                'type': term.content_type,
                'explanation': term.explanation,
                'image': term.image.url if term.image else '',
                'audio': term.audio_file.url if term.audio_file else '',
                'video': term.video_file.url if term.video_file else '',
                'youtube': term.youtube_url or '',
                'link': term.external_link or ''
            }
        context['terms_json'] = terms_data
        return context
