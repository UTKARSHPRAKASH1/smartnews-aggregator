import django_filters
from .models import Article, Category, NewsSource
from django import forms

class ArticleFilter(django_filters.FilterSet):
    # Filter by title (search)
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Search by Keyword',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., AI or Sports'})
    )

    # Filter by category
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Category'
    )

    # Filter by source
    source = django_filters.ModelChoiceFilter(
        queryset=NewsSource.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Source'
    )

    # Filter by date range
    start_date = django_filters.DateFilter(
        field_name='published_at',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='From Date'
    )
    end_date = django_filters.DateFilter(
        field_name='published_at',
        lookup_expr='lte',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='To Date'
    )

    class Meta:
        model = Article
        fields = ['title', 'category', 'source', 'start_date', 'end_date']
