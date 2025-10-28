from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic import ListView, DetailView
from .models import Article, Category, UserPreference
from .forms import UserPreferenceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .filters import ArticleFilter
from django.views import View
from django.shortcuts import get_object_or_404
from .models import SavedArticle, Article
from django.http import HttpResponseRedirect


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home') # We will create 'home' URL later

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

def logout_view(request):
    logout(request)
    return redirect('home') # Redirect to home after logout

def home_view(request):
    trending_articles = Article.objects.order_by('-view_count', '-published_at')[:5]
    personalized_articles = None

    if request.user.is_authenticated:
        try:
            preferences = request.user.preferences
            user_categories = preferences.categories.all()
            if user_categories.exists():
                personalized_articles = Article.objects.filter(category__in=user_categories).order_by('-published_at')[:10]
            else:
                # If no preferences, show latest
                personalized_articles = Article.objects.order_by('-published_at')[:10]
        except UserPreference.DoesNotExist:
            # Handle case where preference object was not created
            personalized_articles = Article.objects.order_by('-published_at')[:10]
    
    # For anonymous users
    if not personalized_articles:
        personalized_articles = Article.objects.order_by('-published_at')[:10]

    context = {
        'trending_articles': trending_articles,
        'personalized_articles': personalized_articles,
    }
    return render(request, 'home.html', context)


class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = ArticleFilter(self.request.GET, queryset=queryset)
        return self.filter.qs # Return the filtered queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter # Pass the filter to the template

        # Preserve filter params during pagination
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        context['filter_params'] = query_params.urlencode()

        return context # Add pagination

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

    def get_object(self, *args, **kwargs):
        # Increment view count
        article = super().get_object(*args, **kwargs)
        Article.objects.filter(pk=article.pk).update(view_count=F('view_count') + 1)
        return article

@login_required
def profile_view(request):
    try:
        preference = request.user.preferences
    except UserPreference.DoesNotExist:
        preference = UserPreference.objects.create(user=request.user)
        
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserPreferenceForm(instance=preference)

    context = {
        'form': form
    }
    return render(request, 'news/profile.html', context)

class SavedArticleListView(LoginRequiredMixin, ListView):
    model = SavedArticle
    template_name = 'news/saved_article_list.html'
    context_object_name = 'saved_articles'
    paginate_by = 10

    def get_queryset(self):
        # Get SavedArticle objects for the current user, ordered by when they were saved
        return SavedArticle.objects.filter(user=self.request.user).order_by('-timestamp')

class ToggleSaveArticleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))

        # Check if it's already saved
        saved_obj, created = SavedArticle.objects.get_or_create(user=request.user, article=article)

        if not created:
            # It was already saved, so unsave it (delete the object)
            saved_obj.delete()

        # Redirect back to the article detail page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('article-detail', kwargs={'pk': article.pk})))