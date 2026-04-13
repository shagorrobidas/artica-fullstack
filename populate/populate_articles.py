import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.articles.models import Article, ArticleSection, Tag
from apps.categories.models import Category, SubCategory

def populate():
    print("Starting population script...")

    # Create Categories
    categories_data = [
        ("প্রযুক্তি", "technology", [("কৃত্রিম বুদ্ধিমত্তা", "ai"), ("ডিজিটাল সাক্ষরতা", "digital-literacy"), ("এডটেক", "edtech")]),
        ("পরিবেশ", "environment", [("জলবায়ু পরিবর্তন", "climate-change"), ("নবায়নযোগ্য শক্তি", "renewable-energy")]),
        ("স্বাস্থ্য", "health", [("সুস্থ জীবনধারা", "healthy-lifestyle"), ("যোগব্যায়াম", "yoga")]),
        ("বিজ্ঞান", "science", [("মহাকাশ গবেষণা", "space-exploration")]),
        ("ইতিহাস ও সংস্কৃতি", "history-culture", [("বাংলার ইতিহাস", "history-of-bengal")]),
        ("কৃষি", "agriculture", [("টেকসই কৃষি", "sustainable-agriculture")]),
    ]

    for cat_name, cat_slug, subcats in categories_data:
        category, _ = Category.objects.get_or_create(name=cat_name, slug=cat_slug)
        for subcat_name, subcat_slug in subcats:
            SubCategory.objects.get_or_create(name=subcat_name, category=category, defaults={"slug": subcat_slug})

    # Create Tags
    tags_data = [
        ("বিজ্ঞান", "science"),
        ("প্রযুক্তি", "technology"),
        ("শিক্ষা", "education"),
        ("জীবনধারা", "lifestyle"),
        ("গবেষণা", "research")
    ]
    tag_objs = []
    for tag_name, tag_slug in tags_data:
        tag, _ = Tag.objects.get_or_create(name=tag_name, defaults={"slug": tag_slug})
        tag_objs.append(tag)

    articles_data = [
        {
            "title": "কৃত্রিম বুদ্ধিমত্তা: আমাদের আগামী দিনের পথচলা",
            "slug": "ai-future-journey",
            "subtitle": "কিভাবে এআই আমাদের জীবন পরিবর্তন করছে",
            "category": "প্রযুক্তি",
            "subcategory": "কৃত্রিম বুদ্ধিমত্তা",
            "body": "<p>কৃত্রিম বুদ্ধিমত্তা বা আর্টিফিশিয়াল ইন্টেলিজেন্স (AI) আজ আমাদের জীবনের প্রতিটি ক্ষেত্রে প্রভাব ফেলছে। স্মার্টফোন থেকে শুরু করে উন্নত রোবটিক্স পর্যন্ত সবখানেই এর উপস্থিতি বিদ্যমান। এটি মানুষের কাজকে সহজতর করছে এবং নতুন নতুন সম্ভাবনার দ্বার উন্মোচন করছে।</p>",
            "excerpt": "কৃত্রিম বুদ্ধিমত্তা বর্তমানে প্রযুক্তির এক অবিচ্ছেদ্য অংশ হয়ে দাঁড়িয়েছে।",
            "status": "published",
        },
        {
            "title": "জলবায়ু পরিবর্তন: বিশ্ব ও আমাদের করণীয়",
            "slug": "climate-change-global-actions",
            "subtitle": "পরিবেশ রক্ষায় বৈশ্বিক উদ্যোগ",
            "category": "পরিবেশ",
            "subcategory": "জলবায়ু পরিবর্তন",
            "body": "<p>জলবায়ু পরিবর্তন বর্তমান বিশ্বের অন্যতম বড় চ্যালেঞ্জ। বৈশ্বিক উষ্ণায়ন বৃদ্ধি পাওয়ার ফলে বরফ গলে যাচ্ছে এবং সমুদ্রপৃষ্ঠের উচ্চতা বাড়ছে। আমাদের উচিত এখনই সচেতন হওয়া এবং কার্বন নিঃসরণ কমানোর জন্য কাজ করা।</p>",
            "excerpt": "জলবায়ু পরিবর্তন রোধে আমাদের এখনই সচেতন হতে হবে।",
            "status": "published",
        },
        {
            "title": "সুস্থ জীবনধারা: প্রতিদিনের কিছু গুরুত্বপূর্ণ অভ্যাস",
            "slug": "healthy-lifestyle-habits",
            "subtitle": "কিভাবে শরীর ও মন সতেজ রাখা যায়",
            "category": "স্বাস্থ্য",
            "subcategory": "সুস্থ জীবনধারা",
            "body": "<p>সুস্থ থাকার জন্য নিয়ম মেনে চলা খুবই জরুরি। প্রতিদিন পর্যাপ্ত পানি পান করা, সুষম খাবার গ্রহণ এবং নিয়মিত ব্যায়াম করা আমাদের রোগমুক্ত রাখতে সাহায্য করে। মানসিক স্বাস্থ্যের দিকেও আমাদের নজর দেওয়া উচিত।</p>",
            "excerpt": "সুস্থ জীবন যাপনের জন্য নিয়মিত ব্যায়াম ও সুষম খাবার অপরিহার্য।",
            "status": "published",
        },
        {
            "title": "মহাকাশ গবেষণা: রহস্যময় মহাবিশ্ব ও মানুষ",
            "slug": "space-exploration-mysteries",
            "subtitle": "নতুন কোনো বাসযোগ্য গ্রহের সন্ধানে",
            "category": "বিজ্ঞান",
            "subcategory": "মহাকাশ গবেষণা",
            "body": "<p>মহাকাশ সব সময়ই মানুষের কাছে রহস্যের আধার। বিজ্ঞানীরা নিরলস ভাবে কাজ করে যাচ্ছেন ভিনগ্রহের প্রাণের সন্ধানে। জেমস ওয়েব টেলিস্কোপ আমাদের মহাবিশ্বের এমন সব ছবি দেখাচ্ছে যা আগে কখনো সম্ভব ছিল না।</p>",
            "excerpt": "মানুষ মহাকাশের রহস্য উন্মোচনে নিরন্তর চেষ্টা চালিয়ে যাচ্ছে।",
            "status": "published",
        },
        {
            "title": "ডিজিটাল সাক্ষরতা: স্মার্ট নাগরিক হওয়ার পথে",
            "slug": "digital-literacy-smart-citizens",
            "subtitle": "ইন্টারনেটের সঠিক ব্যবহার ও নিরাপত্তা",
            "category": "প্রযুক্তি",
            "subcategory": "ডিজিটাল সাক্ষরতা",
            "body": "<p>বর্তমান যুগে কেবল লিখতে বা পড়তে পারাটাই যথেষ্ট নয়। ডিজিটাল প্রযুক্তির ব্যবহার জানা এখন সময়ের দাবি। ডিজিটাল সাক্ষরতা আমাদের অনলাইনে নিরাপদে থাকতে এবং তথ্য প্রযুক্তির সর্বোচ্চ সুবিধা নিতে সাহায্য করে।</p>",
            "excerpt": "ডিজিটাল যুগে উন্নতির জন্য প্রযুক্তিগত জ্ঞান থাকা অপরিহার্য।",
            "status": "published",
        },
        {
            "title": "বাংলার প্রাচীন ইতিহাস: এক গৌরবময় অতীত",
            "slug": "ancient-history-of-bengal",
            "subtitle": "মহাস্থানগড় থেকে মুঘল আমল",
            "category": "ইতিহাস ও সংস্কৃতি",
            "subcategory": "বাংলার ইতিহাস",
            "body": "<p>বাংলার ইতিহাস অত্যন্ত প্রাচীন এবং সমৃদ্ধ। এই জনপদে পাল, সেন এবং মুঘলদের রাজত্ব ছিল। মহাস্থানগড় ও ময়নামতির মতো প্রত্নতাত্ত্বিক নিদর্শনগুলো আমাদের অতীতের সাক্ষ্য বহন করছে। আমাদের এই ঐতিহ্যকে রক্ষা করা উচিত।</p>",
            "excerpt": "বাংলার সমৃদ্ধ ইতিহাস ও ঐতিহ্য আমাদের গর্ব।",
            "status": "published",
        },
        {
            "title": "টেকসই কৃষি: আগামীর খাদ্য নিরাপত্তা",
            "slug": "sustainable-agriculture-food-security",
            "subtitle": "প্রযুক্তি ও প্রকৃতির সমন্বয়",
            "category": "কৃষি",
            "subcategory": "টেকসই কৃষি",
            "body": "<p>ক্রমবর্ধমান জনসংখ্যার জন্য খাদ্যের চাহিদা মেটাতে টেকসই কৃষি পদ্ধতির বিকল্প নেই। জৈব সারের ব্যবহার এবং বৈজ্ঞানিক পদ্ধতিতে চাষাবাদ জমির উর্বরতা বজায় রাখতে সাহায্য করে। এটি পরিবেশের ভারসাম্যও বজায় রাখে।</p>",
            "excerpt": "খাদ্য নিরাপত্তা নিশ্চিত করতে আধুনিক ও টেকসই কৃষি পদ্ধতি জরুরি।",
            "status": "published",
        },
        {
            "title": "যোগব্যায়াম: শরীর ও মনের প্রশান্তি",
            "slug": "yoga-for-body-and-mind",
            "subtitle": "মানসিক চাপ কমাতে যোগব্যায়ামের ভূমিকা",
            "category": "স্বাস্থ্য",
            "subcategory": "যোগব্যায়াম",
            "body": "<p>যোগব্যায়াম কেবল শারীরিক কসরত নয়, এটি এক ধরণের ধ্যান। নিয়মিত ইয়োগা বা যোগব্যায়াম করলে শরীরের নমনীয়তা বাড়ে এবং মন শান্ত হয়। এটি রক্তচাপ নিয়ন্ত্রণে এবং অনিদ্রা দূর করতে সহায়ক।</p>",
            "excerpt": "মন ও শরীরের প্রশান্তির জন্য যোগব্যায়াম অত্যন্ত কার্যকর।",
            "status": "published",
        },
        {
            "title": "নবায়নযোগ্য শক্তি: পরিবেশবান্ধব ভবিষ্যৎ",
            "slug": "renewable-energy-future",
            "subtitle": "সৌরশক্তি ও বায়ুশক্তির ব্যবহার",
            "category": "পরিবেশ",
            "subcategory": "নবায়নযোগ্য শক্তি",
            "body": "<p>ফসিল ফুয়েল বা জীবাশ্ম জ্বালানি ফুরিয়ে আসছে। তাই আমাদের নবায়নযোগ্য শক্তির দিকে ঝুঁকতে হচ্ছে। সৌরশক্তি এবং বায়ুশক্তি পরিবেশের কোনো ক্ষতি করে না এবং এটি দীর্ঘস্থায়ী। এটি পৃথিবীকে দূষণমুক্ত রাখতে সাহায্য করবে।</p>",
            "excerpt": "পরিবেশ বান্ধব শক্তির ব্যবহারই ভবিষ্যৎকে নিরাপদ করবে।",
            "status": "published",
        },
        {
            "title": "শিক্ষা গবেষণায় প্রযুক্তি: একটি নতুন দিগন্ত",
            "slug": "edtech-new-horizons",
            "subtitle": "স্মার্ট ক্লাসরুম ও অনলাইন লার্নিং",
            "category": "প্রযুক্তি",
            "subcategory": "এডটেক",
            "body": "<p>প্রযুক্তি শিক্ষার ধরণ পাল্টে দিয়েছে। এখন বিশ্বের যেকোনো প্রান্ত থেকে যেকোনো কোর্স করা সম্ভব। লার্নিং ম্যানেজমেন্ট সিস্টেম এবং স্মার্ট ক্লাসরুম শিক্ষার্থীদের শেখার প্রক্রিয়াকে আরও সহজ ও আনন্দদায়ক করেছে।</p>",
            "excerpt": "শিক্ষা ক্ষেত্রে প্রযুক্তির ব্যবহার জ্ঞান অর্জনের সুযোগকে প্রসারিত করেছে।",
            "status": "published",
        },
    ]

    for item in articles_data:
        cat = Category.objects.get(name=item["category"])
        subcat = SubCategory.objects.get(name=item["subcategory"])
        
        article, created = Article.objects.get_or_create(
            title=item["title"],
            defaults={
                "slug": item["slug"],
                "subtitle": item["subtitle"],
                "category": cat,
                "subcategory": subcat,
                "body": item["body"],
                "excerpt": item["excerpt"],
                "status": item["status"],
                "published_at": timezone.now() - timedelta(days=random.randint(0, 30)),
                "author": "অ্যাডমিন",
            }
        )
        
        if created:
            # Add random tags
            article.tags.add(*random.sample(tag_objs, k=2))
            
            # Add some sections
            ArticleSection.objects.create(
                article=article,
                title="ভূমিকা",
                content=f"<p>{item['title']} এর উপর একটি বিস্তারিত আলোচনা।</p>",
                order=1
            )
            ArticleSection.objects.create(
                article=article,
                title="বিশ্লেষণ",
                content="<p>এখানে আমরা বিষয়টি নিয়ে আরও গভীরে আলোচনা করব। বর্তমান প্রেক্ষিতে এর গুরুত্ব অপরিসীম।</p>",
                order=2
            )
            print(f"Created article: {item['title']}")
        else:
            print(f"Article already exists: {item['title']}")

    print("Population completed successfully!")

if __name__ == "__main__":
    populate()
