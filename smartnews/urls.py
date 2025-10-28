from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Import built-in views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')), # Include your app's URLs
    
    # Add built-in password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
