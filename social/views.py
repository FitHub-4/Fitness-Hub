from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from .models import Connection, Message


@login_required
def social_hub(request):
    user = request.user
    partners = Connection.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        connection_type='partner',
        status='accepted',
    )
    rivals = Connection.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        connection_type='rival',
        status='accepted',
    )
    pending_incoming = Connection.objects.filter(
        to_user=user, status='pending',
    )
    pending_outgoing = Connection.objects.filter(
        from_user=user, status='pending',
    )

    recent = Message.objects.filter(
        Q(sender=user) | Q(recipient=user),
    ).select_related('sender', 'recipient').order_by('-timestamp')[:20]
    seen_pairs = set()
    conversations = []
    for msg in recent:
        other = msg.recipient if msg.sender == user else msg.sender
        if other.pk not in seen_pairs:
            seen_pairs.add(other.pk)
            conversations.append({
                'user': other,
                'last_message': msg.content[:80],
                'timestamp': msg.timestamp,
                'unread': Message.objects.filter(
                    sender=other, recipient=user, is_read=False,
                ).count(),
            })

    return render(request, 'social/hub.html', {
        'partners': partners,
        'rivals': rivals,
        'pending_incoming': pending_incoming,
        'pending_outgoing': pending_outgoing,
        'conversations': conversations,
    })


@login_required
def search_users(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query),
        ).exclude(pk=request.user.pk)[:20]

    existing = set()
    for c in Connection.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
    ):
        if c.from_user == request.user:
            existing.add(f"{c.to_user.pk}:{c.connection_type}")
        else:
            existing.add(f"{c.from_user.pk}:{c.connection_type}")

    return render(request, 'social/search.html', {
        'query': query,
        'results': results,
        'existing': existing,
    })


@login_required
def send_connection(request):
    if request.method != 'POST':
        return redirect('social-hub')
    user_id = request.POST.get('user_id')
    conn_type = request.POST.get('type')
    if conn_type not in ('partner', 'rival'):
        return redirect('social-hub')
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        return redirect('social-hub')

    Connection.objects.update_or_create(
        from_user=request.user,
        to_user=target,
        connection_type=conn_type,
        defaults={'status': 'pending'},
    )
    return redirect(request.POST.get('next', 'social-hub'))


@login_required
def respond_connection(request):
    if request.method != 'POST':
        return redirect('social-hub')
    conn_id = request.POST.get('conn_id')
    action = request.POST.get('action')
    conn = get_object_or_404(Connection, pk=conn_id, to_user=request.user, status='pending')

    if action == 'accept':
        conn.status = 'accepted'
        conn.save()
    elif action == 'reject':
        conn.status = 'rejected'
        conn.save()
    return redirect('social-hub')


@login_required
def remove_connection(request):
    if request.method != 'POST':
        return redirect('social-hub')
    conn_id = request.POST.get('conn_id')
    conn = get_object_or_404(
        Connection, pk=conn_id,
        status='accepted',
    )
    if conn.from_user != request.user and conn.to_user != request.user:
        return redirect('social-hub')
    conn.delete()
    return redirect('social-hub')


@login_required
def chat(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect('social-hub')

    Message.objects.filter(
        sender=other, recipient=request.user, is_read=False,
    ).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user, recipient=other, content=content,
            )
            return redirect('chat', username=username)
        return redirect('chat', username=username)

    qs = Message.objects.filter(
        Q(sender=request.user, recipient=other) |
        Q(sender=other, recipient=request.user),
    ).select_related('sender')

    last = qs.last()
    last_msg_id = last.pk if last else 0

    return render(request, 'social/chat.html', {
        'other': other,
        'messages': qs,
        'last_msg_id': last_msg_id,
    })


@login_required
def api_send_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    username = request.POST.get('username', '')
    content = request.POST.get('content', '').strip()
    if not content or not username:
        return JsonResponse({'error': 'Missing fields'}, status=400)
    other = get_object_or_404(User, username=username)
    msg = Message.objects.create(
        sender=request.user, recipient=other, content=content,
    )
    return JsonResponse({
        'ok': True,
        'id': msg.pk,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%b %d, %Y at %I:%M %p'),
        'sender': msg.sender.username,
    })


@login_required
def api_get_messages(request, username):
    other = get_object_or_404(User, username=username)
    after = request.GET.get('after', 0)
    try:
        after = int(after)
    except (ValueError, TypeError):
        after = 0

    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other) |
        Q(sender=other, recipient=request.user),
        pk__gt=after,
    ).select_related('sender').order_by('timestamp')

    Message.objects.filter(
        sender=other, recipient=request.user, is_read=False,
    ).update(is_read=True)

    return JsonResponse({
        'messages': [
            {
                'id': m.pk,
                'content': m.content,
                'timestamp': m.timestamp.strftime('%b %d, %Y at %I:%M %p'),
                'sender': m.sender.username,
                'is_mine': m.sender == request.user,
            }
            for m in messages
        ],
    })
