"""Optional LLM-powered responder via OpenRouter (OpenAI-compatible API).

Falls back silently to None so the caller can use the rule-based system instead.
"""

from openai import OpenAI
from django.conf import settings


def get_llm_response(user_input: str, user=None) -> str | None:
    """Return an AI-generated reply, or None if unavailable / error."""
    api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    if not api_key:
        return None

    model = getattr(settings, 'OPENROUTER_MODEL', 'openai/gpt-4o-mini')
    system_prompt = _build_system_prompt(user)

    try:
        client = OpenAI(
            base_url='https://openrouter.ai/api/v1',
            api_key=api_key,
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input},
            ],
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None


def _build_system_prompt(user) -> str:
    """Build a system prompt describing the app and the assistant's role."""
    name = ''
    if user and getattr(user, 'is_authenticated', False):
        name = user.first_name or user.username

    from . import knowledge

    features_lines = []
    for key, feat in knowledge.APP_FEATURES.items():
        features_lines.append(f"- {feat['title']} ({feat['path']}): {feat['summary']}")
    features_str = '\n'.join(features_lines)

    return (
        f"You are the Fitness Hub Coach — a helpful fitness assistant for the "
        f"Fitness Hub workout application. "
        f"{'The user is ' + name + '.' if name else 'The user is not signed in.'}\n\n"
        f"App features:\n{features_str}\n\n"
        f"Rules:\n"
        f"- Keep responses concise (2-5 sentences).\n"
        f"- You can use **bold** for emphasis.\n"
        f"- Never give medical diagnoses or prescribe medication.\n"
        f"- Always encourage safe exercise practices.\n"
        f"- If asked about something outside fitness/nutrition/app-help, politely decline.\n"
        f"- Do not mention that you are an AI or LLM.\n"
        f"- Do not mention specific pricing or unavailable features.\n"
        f"- Guide users to /users/settings/ for account/password changes.\n"
        f"- For exercise technique, give brief form cues and safety notes."
    )
