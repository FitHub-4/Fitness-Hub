from django.db import models
from django.conf import settings


class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('workout_count', 'Workout Count'),
        ('streak', 'Streak'),
        ('volume', 'Volume'),
        ('exercises', 'Exercises'),
        ('nutrition', 'Nutrition'),
        ('goals', 'Goals'),
    ]

    code = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=8, default='🏆')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    threshold = models.PositiveIntegerField(help_text="Value to reach (workouts, streak days, etc.)")
    badge_color = models.CharField(max_length=20, default='emerald')

    class Meta:
        ordering = ['category', 'threshold']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='user_achievements')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')
        ordering = ['-unlocked_at']

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
