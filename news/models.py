# news/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
import math

class CustomUser(AbstractUser):
    # You can add fields like profile_picture, bio etc. later
    pass

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NewsSource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=500)
    rss_feed_url = models.URLField(max_length=500, blank=True, null=True, help_text="For RSS-based sources")

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True, null=True)
    source_url = models.URLField(max_length=1000, unique=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    published_at = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    
    reading_time = models.PositiveSmallIntegerField(default=0, help_text="Estimated reading time in minutes")
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    
    def get_reading_time(self):
        """Calculates reading time based on word count."""
        if self.content:
            word_count = len(self.content.split())
            return math.ceil(word_count / 200) # Assuming 200 WPM
        return 0

    def save(self, *args, **kwargs):
        if not self.reading_time:
            self.reading_time = self.get_reading_time()
        super().save(*args, **kwargs)

class UserPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="preferences")
    categories = models.ManyToManyField(Category, blank=True, help_text="Categories user is interested in")

    def __str__(self):
        return f"{self.user.username}'s Preferences"

class SavedArticle(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved_articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="saved_by_users")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can't save the same article twice
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} saved {self.article.title}"