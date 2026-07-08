import logging
from typing import Optional

from django.conf import settings
from groq import Groq

logger = logging.getLogger(__name__)


def get_groq_response(prompt: str, *, model: Optional[str] = None) -> Optional[str]:
    """Return a Groq completion for the given prompt, or None if unavailable."""
    api_key = getattr(settings, 'GROQ_API_KEY', '').strip()
    model = (model or getattr(settings, 'GROQ_MODEL', 'llama-3.1-8b-instant')).strip()
    if not api_key:
        logger.warning('GROQ_API_KEY is not configured')
        return None

    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are a helpful fitness and nutrition assistant for Fitness Hub. '
                        'Answer clearly, concisely, and safely, and if a question is outside fitness or nutrition, '
                        'gently redirect the user back to fitness-related topics.'
                    ),
                },
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return completion.choices[0].message.content.strip()
    except Exception as exc:
        logger.warning('Groq request failed: %s', exc)
        return None
