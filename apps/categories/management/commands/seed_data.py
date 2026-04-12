import string
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.categories.models import Category, SubCategory, SubSubCategory
from apps.articles.models import Article, Tag, ArticleSection
from apps.media_manager.models import ArticleMedia
from apps.glossary.models import InteractiveTerm, ArticleTermMapping
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeds the database with sample data for EduPlatform'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Ensure superuser exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin" with password "admin123"'))

        # Create Categories
        science, _ = Category.objects.get_or_create(name='Science', description='Explore the wonders of the universe.')
        tech, _ = Category.objects.get_or_create(name='Technology', description='Latest in tech.')
        
        # SubCategories
        physics, _ = SubCategory.objects.get_or_create(name='Physics', category=science)
        ai, _ = SubCategory.objects.get_or_create(name='Artificial Intelligence', category=tech)
        
        # SubSubCategories
        quantum, _ = SubSubCategory.objects.get_or_create(name='Quantum Mechanics', subcategory=physics)

        # Tags
        tag1, _ = Tag.objects.get_or_create(name='Innovation')
        tag2, _ = Tag.objects.get_or_create(name='Future')

        # Interactive Terms
        term1, _ = InteractiveTerm.objects.get_or_create(
            term='Entanglement',
            defaults={
                'explanation': '<p>Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles are generated, interact, or share spatial proximity in ways such that the quantum state of each particle cannot be described independently of the state of the others.</p>'
            }
        )
        term2, _ = InteractiveTerm.objects.get_or_create(
            term='Neural Networks',
            defaults={
                'explanation': '<p>A neural network is a network or circuit of biological neurons, or, in a modern sense, an artificial neural network, composed of artificial neurons or nodes.</p>'
            }
        )

        # Articles
        article_body_1 = """
        <p>In modern physics, the concept of Entanglement challenges our classical understanding of the universe. It suggests that spatial separation does not limit the profound connection between certain particles.</p>
        <p>This has immense implications for the future of quantum computing and secure communications.</p>
        """
        article1, _ = Article.objects.get_or_create(
            title='Understanding Quantum Connections',
            defaults={
                'subtitle': 'A deep dive into paired particles',
                'category': science,
                'subcategory': physics,
                'subsubcategory': quantum,
                'excerpt': 'Learn about the spooky action at a distance that defines modern physics.',
                'body': article_body_1,
                'status': 'published',
                'published_at': timezone.now(),
            }
        )
        article1.tags.add(tag1, tag2)
        
        ArticleTermMapping.objects.get_or_create(article=article1, term=term1)

        ArticleSection.objects.get_or_create(
            article=article1, title='Historical Context',
            defaults={'content': '<p>Einstein referred to this as "spooky action at a distance", refusing to believe that such seemingly faster-than-light coordination could occur.</p>'}
        )

        ArticleMedia.objects.get_or_create(
            article=article1, media_type='youtube', label='Watch the Primer',
            defaults={'youtube_url': 'https://www.youtube.com/watch?v=ZuvK-od647c'}
        )

        self.stdout.write(self.style.SUCCESS('Database successfully seeded with demo data!'))
