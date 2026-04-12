from django.db import models
from apps.articles.models import Article

class ArticleMedia(models.Model):
    MEDIA_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('youtube', 'YouTube'),
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    label = models.CharField(max_length=100, help_text="Button text/label (e.g., 'View Diagram')")
    
    # Conditional fields based on media_type
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='article_media/images/', blank=True, null=True)
    audio_file = models.FileField(upload_to='article_media/audio/', blank=True, null=True)
    video_file = models.FileField(upload_to='article_media/video/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True, help_text="Provide standard YouTube URL")
    
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Article Media'

    def __str__(self):
        return f"{self.article.title} - {self.get_media_type_display()} ({self.label})"
