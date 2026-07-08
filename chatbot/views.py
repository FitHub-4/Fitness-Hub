"""HTTP views for the Fitness Hub chatbot.

Provides a full-page chat (`/chatbot/`) and a JSON API endpoint
(`/chatbot/api/`) used by both the full page and the floating widget.
"""

import json
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from groq import Groq, APIStatusError, APIConnectionError

from .models import ChatSession, ChatMessage
from . import responder
from .groq_utils import get_groq_response

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_or_create_session(request) -> ChatSession:
    """Return the user’s current chat session, creating it if needed."""
    user = request.user if request.user.is_authenticated else None
    if user is not None:
        session, _ = ChatSession.objects.get_or_create(user=user)
        return session

    # Anonymous: pin to a session_key.
    if not request.session.session_key:
        request.session.save()
    key = request.session.session_key
    session, _ = ChatSession.objects.get_or_create(session_key=key, user=None)
    return session


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

@require_GET
def chat_page(request):
    """Render the full chat page."""
    session = _get_or_create_session(request)
    recent = list(
        session.messages.order_by('created_at')[:200]
    )
    return render(request, 'chatbot/chat.html', {
        'session': session,
        'recent': recent,
    })


@csrf_exempt
@require_POST
def chat_api(request):
    """Accept JSON `{message: "..."}` and return JSON `{reply, intent, refused, reason, suggestions}`."""
    try:
        payload = json.loads(request.body or '{}')
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('invalid json')

    text = (payload.get('message') or '').strip()
    session = _get_or_create_session(request)
    result = responder.respond(text, user=request.user)

    # Log user message and bot reply
    if text:
        ChatMessage.objects.create(session=session, role='user', content=text)
    ChatMessage.objects.create(
        session=session,
        role='bot',
        content=result['reply'],
        intent=result['intent'],
    )

    return JsonResponse({
        'reply': result['reply'],
        'intent': result['intent'],
        'refused': result['refused'],
        'reason': result['reason'],
    })


@csrf_exempt
@require_POST
def groq_chat_view(request):
    """Accept a prompt and return a Groq-generated response as JSON."""
    try:
        payload = json.loads(request.body or '{}')
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('invalid json')

    prompt = (payload.get('prompt') or payload.get('message') or '').strip()
    if not prompt:
        return JsonResponse({'error': 'Prompt is required.'}, status=400)

    reply = get_groq_response(prompt)
    if reply is None:
        return JsonResponse({'error': 'Groq is not available right now.'}, status=502)

    return JsonResponse({'reply': reply})


@csrf_exempt
@require_POST
def voice_assistant_view(request):
    """Accept microphone audio, transcribe it with Groq Whisper, generate a reply, and return speech audio."""
    if 'audio' not in request.FILES:
        return JsonResponse({'error': 'No audio file uploaded.'}, status=400)

    audio_file = request.FILES['audio']
    api_key = getattr(settings, 'GROQ_API_KEY', '').strip()
    if not api_key:
        return JsonResponse({'error': 'Groq API key is not configured.'}, status=500)

    try:
        client = Groq(api_key=api_key)

        with NamedTemporaryFile(suffix=Path(audio_file.name).suffix or '.webm', delete=False) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            transcription = client.audio.transcriptions.create(
                file=(tmp_path, audio_file.read()),
                model='whisper-large-v3-turbo',
                language='en',
            )
            user_text = getattr(transcription, 'text', '').strip()
            if not user_text:
                return JsonResponse({'error': 'No speech detected.'}, status=400)
        finally:
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except Exception:
                pass

        llm_response = client.chat.completions.create(
            model=getattr(settings, 'GROQ_MODEL', 'llama-3.1-8b-instant'),
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a friendly, highly concise fitness and nutrition coach. Answer in under 3 sentences.',
                },
                {'role': 'user', 'content': user_text},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        answer_text = llm_response.choices[0].message.content.strip()

        speech_response = client.audio.speech.create(
            model='canopylabs/orpheus-v1-english',
            voice='austin',
            input=answer_text,
            response_format='wav',
        )

        audio_bytes = speech_response.read()
        return HttpResponse(audio_bytes, content_type='audio/wav')
    except APIStatusError as exc:
        logger.warning('Groq API status error: %s', exc)
        return JsonResponse({'error': f'Groq API error: {exc}'}, status=502)
    except APIConnectionError as exc:
        logger.warning('Groq API connection error: %s', exc)
        return JsonResponse({'error': f'Groq connection error: {exc}'}, status=502)
    except Exception as exc:
        logger.exception('Voice assistant pipeline failed')
        return JsonResponse({'error': f'Voice processing failed: {exc}'}, status=500)
