from django.core.management.base import BaseCommand
from achievements.models import Achievement


ACHIEVEMENTS = [
    # Workout count
    {'code': 'first_workout', 'name': 'First Steps', 'description': 'Complete your first workout.', 'icon': '🌱', 'category': 'workout_count', 'threshold': 1, 'badge_color': 'emerald'},
    {'code': 'ten_workouts', 'name': 'Getting Started', 'description': 'Complete 10 workouts.', 'icon': '🔥', 'category': 'workout_count', 'threshold': 10, 'badge_color': 'sky'},
    {'code': 'fifty_workouts', 'name': 'Dedicated', 'description': 'Complete 50 workouts.', 'icon': '💪', 'category': 'workout_count', 'threshold': 50, 'badge_color': 'violet'},
    {'code': 'hundred_workouts', 'name': 'Century Club', 'description': 'Complete 100 workouts.', 'icon': '🏆', 'category': 'workout_count', 'threshold': 100, 'badge_color': 'amber'},
    {'code': 'five_hundred_workouts', 'name': 'Elite', 'description': 'Complete 500 workouts.', 'icon': '👑', 'category': 'workout_count', 'threshold': 500, 'badge_color': 'rose'},
    # Streaks
    {'code': 'streak_3', 'name': 'Threepeat', 'description': 'Maintain a 3-day streak.', 'icon': '📅', 'category': 'streak', 'threshold': 3, 'badge_color': 'emerald'},
    {'code': 'streak_7', 'name': 'Week Warrior', 'description': 'Maintain a 7-day streak.', 'icon': '📆', 'category': 'streak', 'threshold': 7, 'badge_color': 'sky'},
    {'code': 'streak_14', 'name': 'Fortnight Force', 'description': 'Maintain a 14-day streak.', 'icon': '🔥', 'category': 'streak', 'threshold': 14, 'badge_color': 'amber'},
    {'code': 'streak_30', 'name': 'Monthly Master', 'description': 'Maintain a 30-day streak.', 'icon': '⭐', 'category': 'streak', 'threshold': 30, 'badge_color': 'violet'},
    {'code': 'streak_60', 'name': 'Iron Will', 'description': 'Maintain a 60-day streak.', 'icon': '💎', 'category': 'streak', 'threshold': 60, 'badge_color': 'cyan'},
    {'code': 'streak_90', 'name': 'Quarter Century', 'description': 'Maintain a 90-day streak.', 'icon': '👑', 'category': 'streak', 'threshold': 90, 'badge_color': 'rose'},
    # Volume
    {'code': 'volume_1k', 'name': 'Light Work', 'description': 'Accumulate 1,000 total volume.', 'icon': '📈', 'category': 'volume', 'threshold': 1000, 'badge_color': 'emerald'},
    {'code': 'volume_5k', 'name': 'Getting Heavy', 'description': 'Accumulate 5,000 total volume.', 'icon': '🏋️', 'category': 'volume', 'threshold': 5000, 'badge_color': 'sky'},
    {'code': 'volume_10k', 'name': 'Volume Leader', 'description': 'Accumulate 10,000 total volume.', 'icon': '💪', 'category': 'volume', 'threshold': 10000, 'badge_color': 'violet'},
    {'code': 'volume_50k', 'name': 'Beast Mode', 'description': 'Accumulate 50,000 total volume.', 'icon': '🦍', 'category': 'volume', 'threshold': 50000, 'badge_color': 'amber'},
    {'code': 'volume_100k', 'name': 'Legendary Volume', 'description': 'Accumulate 100,000 total volume.', 'icon': '👑', 'category': 'volume', 'threshold': 100000, 'badge_color': 'rose'},
]


class Command(BaseCommand):
    help = 'Seed achievement definitions.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding achievements...')
        for a in ACHIEVEMENTS:
            Achievement.objects.update_or_create(code=a['code'], defaults=a)
        self.stdout.write(self.style.SUCCESS(f'  + {len(ACHIEVEMENTS)} achievements ready'))
