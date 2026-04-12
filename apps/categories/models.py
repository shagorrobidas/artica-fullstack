from django.db import models
from django.utils.text import slugify

class BaseCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(BaseCategory):
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    class Meta(BaseCategory.Meta):
        verbose_name_plural = 'Categories'

class SubCategory(BaseCategory):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta(BaseCategory.Meta):
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return f"{self.category.name} > {self.name}"

class SubSubCategory(BaseCategory):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subsubcategories')

    class Meta(BaseCategory.Meta):
        verbose_name_plural = 'Sub-Sub Categories'

    def __str__(self):
        return f"{self.subcategory.category.name} > {self.subcategory.name} > {self.name}"
