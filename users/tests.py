from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class UserRegistrationTests(TestCase):
    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'Testpass123!',
                'password2': 'Testpass123!',
                'age': 25,
                'height_ft': '5.75',
                'weight_kg': '70',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

        profile = Profile.objects.filter(user=user).first()
        self.assertIsNotNone(profile)
        self.assertEqual(profile.age, 25)
        self.assertEqual(str(profile.height_ft), '5.75')
        self.assertEqual(str(profile.weight_kg), '70.00')
