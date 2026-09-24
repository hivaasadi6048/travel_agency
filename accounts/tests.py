from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class AccountsTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
