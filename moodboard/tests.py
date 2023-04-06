from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post

class PostCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_create_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-create'), {
            'author': self.user,
            'title': 'Test post',
            'text': 'This is a test post',
            'published_date': timezone.now(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post-detail', args=[1]))

    def test_create_blank_post(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('post-create'), {})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'text', 'This field is required.')
