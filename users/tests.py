from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            telegram_id='123456789'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.telegram_id, '123456789')
        self.assertIsNone(self.user.username)

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')


class UserRegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_success(self):
        data = {
            'email': 'newuser@example.com',
            'telegram_id': '987654321',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().email, 'newuser@example.com')

    def test_register_user_password_mismatch(self):
        data = {
            'email': 'failuser@example.com',
            'telegram_id': '111111111',
            'password': 'pass123',
            'password_confirm': 'pass456'
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
