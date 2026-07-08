from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Exercise, ExerciseCompletion
from progress.models import UserWorkoutStats


class ExerciseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='athlete', password='athletepass')
        self.exercise = Exercise.objects.create(
            name='Push-Up',
            category='chest',
            goal='general',
            default_reps=10,
            default_sets=3,
        )

    def test_quick_complete_logs_exercise_and_updates_stats(self):
        self.client.login(username='athlete', password='athletepass')
        response = self.client.post(
            reverse('exercise-complete', args=[self.exercise.slug]),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        completion = ExerciseCompletion.objects.filter(user=self.user, exercise=self.exercise).first()
        self.assertIsNotNone(completion)

        stats = UserWorkoutStats.objects.get(user=self.user)
        self.assertEqual(stats.total_workouts, 1)
        self.assertEqual(stats.current_streak, 1)
        self.assertEqual(stats.longest_streak, 1)
