import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from goals.models import Goal
from progress.models import ProgressRecord, UserWorkoutStats
from exercises.models import ExerciseCompletion
from core.utils import get_current_goal
from progress.views import generate_focus_alignment_message

logger = logging.getLogger(__name__)


def get_next_exercise(goal):
    if not goal:
        return None
    return goal.assigned_exercises.order_by('id').first()


def compute_goal_readiness(goal, user):
    if not goal:
        return 0
    if goal.progress_percent:
        return min(100, max(0, goal.progress_percent))

    logs = ProgressRecord.objects.filter(user=user, goal=goal)
    assigned = goal.assigned_exercises.count()
    if assigned == 0:
        return 0
    completed_ratio = min(1.0, logs.count() / max(1, assigned))
    return int(completed_ratio * 100)


@login_required
def index(request):
    goal = get_current_goal(request)
    next_exercise = get_next_exercise(goal)
    readiness = compute_goal_readiness(goal, request.user)
    focus_alignment = generate_focus_alignment_message(request.user, goal)

    # Safe workout stats lookup
    try:
        stats = request.user.workout_stats
    except UserWorkoutStats.DoesNotExist:
        stats = None

    # Recent completions
    recent_completions = ExerciseCompletion.objects.filter(
        user=request.user
    ).select_related('exercise').order_by('-date')[:10]

    # Weekly completion count
    week_ago = timezone.now().date() - timedelta(days=7)
    weekly_completions = ExerciseCompletion.objects.filter(
        user=request.user, date__gte=week_ago
    ).count()

    # Workout stats
    today = timezone.now().date()
    completed_today = ExerciseCompletion.objects.filter(
        user=request.user, date=today
    ).count()

    return render(
        request,
        'dashboard/index.html',
        {
            'goal': goal,
            'next_exercise': next_exercise,
            'readiness': readiness,
            'focus_alignment': focus_alignment,
            'stats': stats,
            'recent_completions': recent_completions,
            'weekly_completions': weekly_completions,
            'completed_today': completed_today,
        },
    )
