from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from apps.categories.models import Category, SubCategory, SubSubCategory

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.CharField(max_length=100, default='Admin')
    
    # Hierarchy relation (only one needs to be set, typically the deepest one applicable)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    subsubcategory = models.ForeignKey(SubSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')

    cover_image = models.ImageField(upload_to='article_covers/')
    body = RichTextField()
    excerpt = models.TextField(blank=True, null=True, help_text="Short summary for lists")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    content = RichTextField()
    order = models.PositiveIntegerField(default=0)
    is_expanded_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.article.title} - {self.title}"
