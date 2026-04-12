import os
import django
import random
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from apps.categories.models import Category, SubCategory
from apps.articles.models import Article, Tag, ArticleSection
from apps.glossary.models import InteractiveTerm, ArticleTermMapping

print("Deleting old objects...")
ArticleSection.objects.all().delete()
Article.objects.all().delete()
Tag.objects.all().delete()

SubCategory.objects.all().delete()
Category.objects.all().delete()

print("Creating 10 dummy items for each model...")

categories = []
for i in range(1, 11):
    c = Category.objects.create(name=f"Dummy Category {i}", description=f"Description {i}")
    categories.append(c)

subcategories = []
for i in range(1, 11):
    sc = SubCategory.objects.create(name=f"Dummy SubCategory {i}", category=categories[i-1], description=f"Description {i}")
    subcategories.append(sc)



tags = []
for i in range(1, 11):
    t = Tag.objects.create(name=f"Dummy Tag {i}")
    tags.append(t)

for i in range(1, 11):
    article = Article.objects.create(
        title=f"Dummy Article {i}",
        subtitle=f"Subtitle for Dummy Article {i}",
        body=f"<p>This is the dummy body content for article {i}.</p>",
        category=random.choice(categories),
        subcategory=random.choice(subcategories),
        status='published',
        cover_image='article_covers/dummy.jpg'  # Providing a dummy string path
    )
    article.tags.set(random.sample(tags, 3))
    
    ArticleSection.objects.create(
        article=article,
        title=f"Dummy Section 1 for Article {i}",
        content=f"<p>Content for section 1 of article {i}.</p>"
    )

print("Created 10 dummy objects for each primary model in apps successfully!")
