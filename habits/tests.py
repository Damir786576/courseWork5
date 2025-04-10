from django.test import TestCase
from django.db.models.signals import post_save
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit, schedule_habit_reminder
from users.models import CustomUser


class HabitModelTest(TestCase):
    def setUp(self):
        post_save.disconnect(receiver=schedule_habit_reminder, sender=Habit)
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            action='Test Habit',
            time='12:00:00',
            place='Home',
            periodicity=1,
            duration=60,
            is_public=True
        )

    def tearDown(self):
        post_save.connect(receiver=schedule_habit_reminder, sender=Habit)

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
        post_save.disconnect(receiver=schedule_habit_reminder, sender=Habit)
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='apiuser',
            email='user@example.com',
            password='pass123'
        )
        self.client.force_authenticate(user=self.user)
        Habit.objects.all().delete()
        Habit.objects.create(user=self.user, action='Private Habit', time='10:00:00', place='Gym', periodicity=1,
                             duration=60, is_public=False)
        Habit.objects.create(user=self.user, action='Public Habit', time='11:00:00', place='Park', periodicity=1,
                             duration=60, is_public=True)

    def tearDown(self):
        post_save.connect(receiver=schedule_habit_reminder, sender=Habit)

    def test_habit_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)