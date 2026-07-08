import json

from django.test import TestCase, override_settings

from .models import ChatSession
from .responder import respond
from .groq_utils import get_groq_response


class ChatbotTests(TestCase):
    def test_chat_api_returns_reply_and_creates_session(self):
        response = self.client.post(
            '/chatbot/api/',
            json.dumps({'message': 'hello'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn('reply', payload)
        self.assertFalse(payload.get('refused'))
        self.assertEqual(payload.get('intent'), 'greeting')

        session = ChatSession.objects.first()
        self.assertIsNotNone(session)
        self.assertEqual(session.messages.count(), 2)

    def test_unknown_question_returns_exact_answer_fallback(self):
        payload = respond('What is the secret to time travel in fitness?')
        self.assertIn('couldn\'t find the exact answer', payload['reply'].lower())

    def test_chat_page_exposes_voice_input_button(self):
        response = self.client.get('/chatbot/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Speak with voice')
        self.assertContains(response, 'Tap to speak')

    @override_settings(GROQ_API_KEY='')
    def test_groq_helper_returns_none_without_configuration(self):
        self.assertIsNone(get_groq_response('Hello from Groq'))
