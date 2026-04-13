from django.db import models
from apps.articles.models import Article


class ArticleMedia(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='media'
    )
    label = models.CharField(
        max_length=100,
        help_text="Button text/label (e.g., 'View Diagram')"
    )

    # Conditional fields based on media_type
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='article_media/images/',
        blank=True,
        null=True
    )
    audio_file = models.FileField(
        upload_to='article_media/audio/',
        blank=True,
        null=True
    )
    video_file = models.FileField(
        upload_to='article_media/video/',
        blank=True,
        null=True
    )
    youtube_url = models.URLField(
        blank=True,
        null=True,
        help_text="Provide standard YouTube URL"
    )

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Article Media'

    def __str__(self):
        return f"{self.article.title} - {self.label}"

    @property
    def youtube_embed_url(self):
        if not self.youtube_url:
            return ""
        if "youtube.com/embed/" in self.youtube_url:
            return self.youtube_url
            
        import re
        # Comprehensive regex to catch berbagai Youtube URL formats
        reg = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(reg, self.youtube_url)
        if match:
            video_id = match.group(1)
            # Use youtube-nocookie.com and add rel=0 to avoid Error 153
            return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&enablejsapi=1"
        return self.youtube_url
