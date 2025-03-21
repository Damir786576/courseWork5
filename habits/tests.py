from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Habit
from users.models import CustomUser

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', password='testpass123')
        self.habit = Habit.objects.create(
            user=self.user,
            action='Test Habit',
            time='12:00:00',
            place='Home',
            periodicity=1,
            duration=60,
            is_public=True
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, 'Test Habit')
        self.assertEqual(self.habit.user.email, 'test@example.com')
        self.assertTrue(self.habit.is_public)

    def test_habit_validation_duration(self):
        with self.assertRaises(Exception):
            Habit.objects.create(
                user=self.user,
                action='Long Habit',
                time='13:00:00',
                place='Office',
                duration=150
            ).full_clean()

    def test_habit_str(self):
        self.assertEqual(str(self.habit), 'Test Habit в 12:00:00 в Home')


class HabitAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email='user@example.com', password='pass123')
        self.client.force_authenticate(user=self.user)
        Habit.objects.create(user=self.user, action='Private Habit', time='10:00:00', place='Gym', is_public=False)
        Habit.objects.create(user=self.user, action='Public Habit', time='11:00:00', place='Park', is_public=True)

    def test_habit_list_authenticated(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['count'], 1)

    def test_public_habit_list(self):
        self.client.logout()
        response = self.client.get('/api/public-habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['action'], 'Public Habit')
