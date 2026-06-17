import logging

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Achievement, UserAchievement

logger = logging.getLogger(__name__)


def check_and_unlock(user, achievement_codes):
    """Check and unlock achievements for a user."""
    unlocked = []
    for code in achievement_codes:
        try:
            achievement = Achievement.objects.get(code=code)
            _, created = UserAchievement.objects.get_or_create(
                user=user, achievement=achievement
            )
            if created:
                unlocked.append(achievement)
        except Achievement.DoesNotExist:
            pass
    return unlocked


def check_workout_achievements(user):
    from exercises.models import ExerciseCompletion
    total = ExerciseCompletion.objects.filter(user=user).count()
    codes = []
    for threshold, code in [(1, 'first_workout'), (10, 'ten_workouts'), (50, 'fifty_workouts'),
                             (100, 'hundred_workouts'), (500, 'five_hundred_workouts')]:
        if total >= threshold:
            codes.append(code)
    return check_and_unlock(user, codes)


def check_streak_achievements(user):
    try:
        stats = user.workout_stats
        streak = stats.longest_streak
    except Exception:
        return []
    codes = []
    for threshold, code in [(3, 'streak_3'), (7, 'streak_7'), (14, 'streak_14'),
                             (30, 'streak_30'), (60, 'streak_60'), (90, 'streak_90')]:
        if streak >= threshold:
            codes.append(code)
    return check_and_unlock(user, codes)


def check_volume_achievements(user):
    from exercises.models import ExerciseCompletion
    from django.db.models import Sum, F, Case, When, Value, FloatField
    total_volume = ExerciseCompletion.objects.filter(user=user).aggregate(
        total=Coalesce(Sum(
            Case(
                When(hold_time_sec__gt=0, then=F('hold_time_sec')),
                default=F('reps'),
                output_field=FloatField(),
            ),
            output_field=FloatField(),
        ), Value(0, output_field=FloatField()))
    )['total'] or 0
    codes = []
    for threshold, code in [(1000, 'volume_1k'), (5000, 'volume_5k'), (10000, 'volume_10k'),
                             (50000, 'volume_50k'), (100000, 'volume_100k')]:
        if total_volume >= threshold:
            codes.append(code)
    return check_and_unlock(user, codes)
