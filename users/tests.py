from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCreationTest(TestCase):
    def test_create_user(self):
        url = reverse('register') # replace 'register' with the actual name of your registration view
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # check that the response is a redirect
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
