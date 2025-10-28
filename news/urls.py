# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # We will create the home_view in Phase 5
    # path('', views.home_view, name='home'), 
    
    # Auth URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('news/', views.ArticleListView.as_view(), name='article-list'),
    path('news/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('profile/', views.profile_view, name='profile'),
    path('saved/', views.SavedArticleListView.as_view(), name='saved-articles'),
    path('news/<int:pk>/save/', views.ToggleSaveArticleView.as_view(), name='toggle-save'),
]
