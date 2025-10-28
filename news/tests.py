from django.test import TestCase
from django.urls import reverse
from .models import CustomUser, Category

class HomeViewTest(TestCase):
    def test_home_view_anonymous(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('personalized_articles', response.context)

    def test_home_view_authenticated(self):
        user = CustomUser.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Personalized Feed')

class CategoryModelTest(TestCase):
    def test_slug_creation(self):
        category = Category.objects.create(name="Health & Wellness")
        self.assertEqual(category.slug, "health-wellness")