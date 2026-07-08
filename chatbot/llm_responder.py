"""Optional LLM-powered responder via OpenAI or OpenRouter.

Falls back silently to None so the caller can use the rule-based system instead.
"""

import logging

from openai import OpenAI
from django.conf import settings

logger = logging.getLogger('chatbot')


def get_llm_response(user_input: str, user=None):
    """Return an AI-generated reply, or None if unavailable / error."""
    openai_api_key = getattr(settings, 'OPENAI_API_KEY', '')
    openai_model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')
    openrouter_api_key = getattr(settings, 'OPENROUTER_API_KEY', '')
    openrouter_model = getattr(settings, 'OPENROUTER_MODEL', 'openai/gpt-4o-mini')

    if openai_api_key:
        provider = 'openai'
        api_key = openai_api_key
        model = openai_model
    elif openrouter_api_key:
        provider = 'openrouter'
        api_key = openrouter_api_key
        model = openrouter_model
    else:
        return None

    system_prompt = _build_system_prompt(user)

    try:
        if provider == 'openai':
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_input},
                ],
                temperature=0.7,
                max_tokens=600,
            )
        else:
            client = OpenAI(
                base_url='https://openrouter.ai/api/v1',
                api_key=api_key,
                timeout=30.0,
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
    except Exception as e:
        logger.warning('LLM request failed: %s', e)
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
        "You are 'Codex Coach,' an elite, certified AI Fitness & Nutrition Expert built for the Fitness Hub platform. "
        "Your goal is to provide highly accurate, professional, encouraging, and scientifically backed answers regarding exercises, workouts, and nutrition.\n\n"
        "CRITICAL INSTRUCTIONS FOR REPLIES:\n"
        "1. EXERCISE ACCURACY: When a user asks about an exercise, detail the target muscle groups, correct form, safety tips, and common mistakes to avoid. "
        "If the exercise exists in our platform's seeded library, enthusiastically guide them on how to utilize it.\n"
        "2. TAILORED & CONTEXTUAL: Never say 'I could not find the exact answer.' If a question is broad, ask intelligent clarifying questions (e.g., fitness level, equipment access) to tailor your advice like a real personal trainer.\n"
        "3. TONAL ARCHITECTURE: Sound like an elite human coach—knowledgeable, motivating, direct, and professional. Avoid sounding mechanical or overly robotic. Use formatting (bullet points, bold text) to make your advice scannable.\n"
        "4. SAFETY GUARDRAILS: Always include a brief, professional medical disclaimer if a user asks about recovering from injuries or executing high-risk movements (e.g., 'Always consult a physician before attempting heavy lifts if you have a history of back issues.').\n"
        "5. SCOPE: Gently guide the user back to fitness, health, habit-building, and nutrition if they attempt to ask about unrelated topics (e.g., coding, politics, celebrity gossip).\n\n"
        f"The user is {'signed in as ' + name if name else 'not signed in'}.\n\n"
        "App features:\n"
        f"{features_str}\n\n"
        "When possible, mention relevant Fitness Hub sections and keep responses focused on the user's request."
    )
