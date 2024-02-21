from django.test import TestCase, Client
from django.urls import reverse
from homepage import views

class TestAdminURL(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_url(self):
        response = self.client.get('/admin/')  # Assurez-vous que l'URL que vous testez correspond à celle que vous avez configurée dans vos URLs
        self.assertEqual(response.status_code, 302)  # Vérifiez que la réponse est 200 (OK)
        self.assertRedirects(response, '/admin/login/?next=/admin/', fetch_redirect_response=False)

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_urls(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_service_url(self):
        response = self.client.get('/service/')
        self.assertEqual(response.status_code, 200)
    
    def test_media_url(self):
        response = self.client.get('/media/')
        self.assertEqual(response.status_code, 200)
