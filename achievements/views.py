from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Achievement, UserAchievement
from . import signals as achv_signals


@login_required
def achievement_list(request):
    achv_signals.check_workout_achievements(request.user)
    achv_signals.check_streak_achievements(request.user)
    achv_signals.check_volume_achievements(request.user)

    all_achievements = Achievement.objects.all()
    unlocked_ids = set(
        UserAchievement.objects.filter(user=request.user)
        .values_list('achievement_id', flat=True)
    )

    achievements_by_category = {}
    for a in all_achievements:
        achievements_by_category.setdefault(a.get_category_display(), []).append({
            'achievement': a,
            'unlocked': a.id in unlocked_ids,
        })

    return render(request, 'achievements/list.html', {
        'achievements_by_category': achievements_by_category,
        'total_unlocked': len(unlocked_ids),
        'total_count': all_achievements.count(),
    })
