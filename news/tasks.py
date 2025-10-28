import os
import requests
import feedparser
from celery import shared_task
from .models import Article, NewsSource, Category
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError

@shared_task
def fetch_news_task():
    print("Starting news fetch task...")
    api_key = os.environ.get('NEWS_API_KEY')

    # --- Fetch from NewsAPI (Example for 'technology') ---
    # Note: NewsAPI free plan is limited. You might fetch by source.
    # Here we'll fetch 'technology' from 'bbc-news'
    try:
        source_name = "BBC News"
        category_name = "Technology"

        # Get or create source and category
        source_obj, _ = NewsSource.objects.get_or_create(name=source_name, defaults={'url': '[https://www.bbc.co.uk/news](https://www.bbc.co.uk/news)'})
        category_obj, _ = Category.objects.get_or_create(name=category_name)

        url = f"[https://newsapi.org/v2/top-headlines?sources=bbc-news&category=](https://newsapi.org/v2/top-headlines?sources=bbc-news&category=){category_name.lower()}&apiKey={api_key}"
        response = requests.get(url)
        data = response.json()

        if data.get('status') == 'ok':
            for item in data.get('articles', []):
                # Check if article already exists
                if Article.objects.filter(source_url=item['url']).exists():
                    continue

                # Parse datetime
                published_at_str = item.get('publishedAt')
                published_at_dt = parse_datetime(published_at_str) if published_at_str else datetime.now()

                Article.objects.create(
                    title=item['title'],
                    content=item.get('description') or item.get('content') or "",
                    source_url=item['url'],
                    image_url=item.get('urlToImage'),
                    published_at=published_at_dt,
                    category=category_obj,
                    source=source_obj
                )
        print(f"Fetched {len(data.get('articles', []))} articles from {source_name}")

    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")

    # --- Fetch from RSS Feeds ---
    rss_sources = NewsSource.objects.filter(rss_feed_url__isnull=False)
    for source in rss_sources:
        try:
            feed = feedparser.parse(source.rss_feed_url)
            for entry in feed.entries:
                if Article.objects.filter(source_url=entry.link).exists():
                    continue

                published_dt = datetime.now()
                if hasattr(entry, 'published_parsed'):
                    published_dt = datetime(*entry.published_parsed[:6])

                Article.objects.create(
                    title=entry.title,
                    content=entry.get('summary') or entry.get('description') or "",
                    source_url=entry.link,
                    image_url=entry.get('media_content', [{}])[0].get('url') or None,
                    published_at=published_dt,
                    source=source
                    # You might need to map feed categories to your categories
                )
            print(f"Fetched {len(feed.entries)} articles from RSS: {source.name}")
        except Exception as e:
            print(f"Error fetching from RSS {source.name}: {e}")

    print("News fetch task finished.")
    return "News fetch complete."