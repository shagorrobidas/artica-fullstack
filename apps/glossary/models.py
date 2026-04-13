from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from apps.articles.models import Article

class InteractiveTerm(models.Model):
    CONTENT_TYPES = (
        ('text', 'Text only (🔍)'),
        ('image', 'Image + Text (🖼️)'),
        ('audio', 'Audio + Text (🔊)'),
        ('video', 'Video + Text (🎥)'),
    )

    term = models.CharField(max_length=100, unique=True, help_text="The word/phrase to highlight")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='text')
    explanation = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='glossary/images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='glossary/audio/', blank=True, null=True)
    video_file = models.FileField(upload_to='glossary/video/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="YouTube URL")
    external_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.term)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.term

class ArticleTermMapping(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='term_mappings')
    term = models.ForeignKey(InteractiveTerm, on_delete=models.CASCADE, related_name='article_mappings')
    occurrence_index = models.PositiveIntegerField(default=0, help_text="0 means highlight all occurrences, 1 means first, etc.")

    class Meta:
        unique_together = ('article', 'term', 'occurrence_index')

    def __str__(self):
        return f"{self.term.term} in {self.article.title}"
