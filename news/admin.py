from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, NewsSource, Article, UserPreference, SavedArticle

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add any custom fields you add to CustomUser here
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ()}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ()}),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'rss_feed_url')
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'category', 'published_at', 'view_count', 'reading_time')
    list_filter = ('source', 'category', 'published_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('categories',) # Makes M2M easier to edit

@admin.register(SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'timestamp')
    list_filter = ('user',)
