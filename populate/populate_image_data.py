import os
import django
from django.utils import timezone
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.articles.models import Article, ArticleSection
from apps.glossary.models import InteractiveTerm, ArticleTermMapping
from apps.categories.models import Category, SubCategory

def populate_clean_article():
    print("Populating full article with stable English slugs...")

    # Ensure Category
    category, _ = Category.objects.get_or_create(name="ক্রাইম", slug="crime")
    subcategory, _ = SubCategory.objects.get_or_create(name="তদন্ত", slug="investigation", category=category)

    # 1. Clean up existing mappings for this article to avoid duplicates
    ArticleTermMapping.objects.filter(article__slug="fortune-mall-gold-theft-solved").delete()

    # 2. Terms with stable English slugs
    terms_info = [
        {
            "term": "সন্দহে", # Note: I'll use the exact spelling in text or fix text
            "slug": "ter-suspicion",
            "type": "text",
            "explanation": "<p>কোনো অপরাধে জড়িত থাকার পরিষ্কার প্রমাণ না থাকলেও পারিপার্শ্বিক অবস্থার ভিত্তিতে কাউকে অভিযুক্ত মনে করা।</p>"
        },
        {
            "term": "Audio",
            "slug": "ter-audio-clip",
            "type": "audio",
            "explanation": "<p>ঘটনার প্রত্যক্ষদর্শীর ধারণকৃত অডিও ক্লিপ। এতে চুরির সময় মার্কেটের পরিস্থিতি ও শব্দ শোনা যাচ্ছে।</p>",
            "file": "glossary/audio/sample_audio.mp3"
        },
        {
            "term": "সমন্বয়কারী",
            "slug": "ter-coordinator",
            "type": "text",
            "explanation": "<p>যিনি বিভিন্ন ব্যক্তি বা দলের মধ্যে কাজের মেলবন্ধন তৈরি করেন বা পরিকল্পনা কার্যকর করেন।</p>"
        },
        {
            "term": "স্বর্ণ",
            "slug": "ter-gold-jewelry",
            "type": "image",
            "explanation": "<p>উদ্ধারকৃত স্বর্ণালংকারের স্থিরচিত্র। ডিবি পুলিশ অভিযানে প্রায় ১৯০ ভরি স্বর্ণ উদ্ধারে সক্ষম হয়েছে।</p>",
            "file": "glossary/images/stolen_gold.png"
        },
        {
            "term": "বোরকা",
            "slug": "ter-burqa",
            "type": "text",
            "explanation": "<p>পরিচয় গোপনের লক্ষ্যে চোরচক্রটি বোরকা পরে শপিং মলে প্রবেশ করেছিল।</p>"
        },
        {
            "term": "তদন্ত",
            "slug": "ter-investigation-video",
            "type": "video",
            "explanation": "<p>ডিবি পুলিশের তদন্ত কার্যক্রমের সারসংক্ষেপ। তারা সিসিটিভি ফুটেজ ও তথ্যপ্রযুক্তির সহায়তায় অপরাধীদের শনাক্ত করে।</p>",
            "youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
        }
    ]

    term_objs = {}
    for data in terms_info:
        # We delete old versions to ensure slugs are correctly updated in DB
        InteractiveTerm.objects.filter(term=data["term"]).delete()
        
        term = InteractiveTerm.objects.create(
            term=data["term"],
            slug=data["slug"],
            content_type=data["type"],
            explanation=data["explanation"],
            image=data.get("file") if data["type"] == 'image' else None,
            audio_file=data.get("file") if data["type"] == 'audio' else None,
            youtube_url=data.get("youtube") if data["type"] == 'video' else None,
            external_link="https://www.google.com/search?q=" + data["slug"] # Demo link
        )
        term_objs[data["term"]] = term
        print(f"Created term: {data['term']} -> {data['slug']}")

    # 3. Full Article Body (Ensure spelling matches terms)
    body_text = """
    <p>রাজধানীর মালিবাগের ফরচুন শপিং মলের 'শম্পা জুয়েলার্স' থেকে স্বর্ণালংকার চুরির চাঞ্চল্যকর ঘটনায় রহস্য উদ্ঘাটন করেছে ঢাকা মহানগর পুলিশের গোয়েন্দা বিভাগ (ডিবি)। দুর্ধর্ষ এই চুরির ঘটনায় জড়িত সন্দেহে চার জনকে গ্রেফতার করা হয়েছে এবং তাদের কাছ থেকে বিপুল পরিমাণ চোরাই স্বর্ণালংকার উদ্ধার করা হয়েছে বলে জানিয়েছে ডিবি।</p>
    
    <p>ডিবির তিনটি টিম টানা ৭২ ঘণ্টা দেশের বিভিন্ন স্থানে অভিযান চালায়। প্রথমে চট্টগ্রাম থেকে শাহিন মাতব্বরকে গ্রেফতার ও ফরিদপুর থেকে স্বর্ণ উদ্ধার করা হয়। পরে বরিশাল থেকে আরও দুই জনকে গ্রেফতার করা হয়েছে। ঢাকা থেকে ডিবি গ্রেফতার করে এই চক্রের সমন্বয়কারী নুরুল ইসলামকে, যে মোটরসাইকেল ব্যবহার করে মার্কেটের রেকি করতো। সিসিটিভি ফুটেজে দেখা যায়, আব্দুল্লাহ এবং তার সহযোগীদের কেউ কেউ বোরকা পরে সুকৌশলে ভেতরে প্রবেশ করেছিল।</p>
    
    <p>তদন্তে জানা যায়, চোরচক্রটি প্রায় তিন মাস ধরে শপিং মলটি পর্যবেক্ষণ (রেকি) করেছিল। ঘটনার দিন রাতে তারা সুকৌশলে ছাদের গ্রিল কেটে ভেতরে প্রবেশ করে এই চুরি সম্পন্ন করে। দোকানের মালিকের দাবি অনুযায়ী দোকানে ৫০০ ভরি স্বর্ণালংকার ছিল। তবে ডিবি পুলিশের অভিযানে ১৯০ ভরি সোনা উদ্ধার হয়েছে। বাকি মালামাল উদ্ধারে তদন্ত অব্যাহত রয়েছে। ডিবি কর্মকর্তাদের মতে, গ্রেফতারকৃতরা পেশাদার চোর এবং তাদের বিরুদ্ধে আগেও এ ধরনের একাধিক মামলা রয়েছে।</p>
    """

    article, created = Article.objects.get_or_create(
        slug="fortune-mall-gold-theft-solved",
        defaults={
            "title": "ফরচুন শপিং মলে ৫০০ ভরি চুরির রহস্য উদ্ঘাটন: চারজন গ্রেফতার",
            "body": body_text,
            "category": category,
            "subcategory": subcategory,
            "status": "published",
            "author": "ডিবি নিউজ",
            "published_at": timezone.now()
        }
    )
    if not created:
        article.body = body_text
        article.save()
    print(f"Ensured article: {article.title}")

    # 4. Map Terms
    for term_name, term_obj in term_objs.items():
        ArticleTermMapping.objects.get_or_create(
            article=article,
            term=term_obj,
            occurrence_index=0
        )
        print(f"Mapped '{term_name}' to article")

    print("\nCleanup and population successful! Modals should work now.")

if __name__ == "__main__":
    populate_clean_article()
