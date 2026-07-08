import json
from pathlib import Path
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import ChatSession
from .responder import respond
from .groq_utils import get_groq_response


class ChatbotTests(TestCase):
    def test_home_page_does_not_expose_voice_coach_launcher(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'id="mic-toggle"')
        self.assertNotContains(response, 'voice_coach.js')

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

    def test_chat_widget_script_contains_voice_handler(self):
        script_path = Path(__file__).resolve().parent.parent / 'static' / 'chatbot' / 'js' / 'chat.js'
        self.assertTrue(script_path.exists())
        script_text = script_path.read_text(encoding='utf-8')
        self.assertIn('attachVoiceInputToSurface', script_text)

    @patch('chatbot.views.Groq')
    def test_voice_endpoint_falls_back_to_text_when_speech_synthesis_fails(self, groq_cls):
        class FakeAudioTranscriptions:
            def create(self, **kwargs):
                return type('Transcription', (), {'text': 'hello there'})()

        class FakeAudioSpeech:
            def create(self, **kwargs):
                raise RuntimeError('tts unavailable')

        class FakeChatCompletions:
            def create(self, **kwargs):
                return type('Completion', (), {
                    'choices': [type('Choice', (), {'message': type('Message', (), {'content': 'I can help with that'})()})]
                })()

        class FakeAudio:
            transcriptions = FakeAudioTranscriptions()
            speech = FakeAudioSpeech()

        class FakeClient:
            audio = FakeAudio()
            chat = type('Chat', (), {'completions': FakeChatCompletions()})()

        groq_cls.return_value = FakeClient()

        response = self.client.post(
            '/chatbot/voice/',
            {'audio': SimpleUploadedFile('test.wav', b'abc', content_type='audio/wav')},
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload['text'], 'I can help with that')
        self.assertEqual(payload['mode'], 'text')

    @override_settings(GROQ_API_KEY='')
    def test_groq_helper_returns_none_without_configuration(self):
        self.assertIsNone(get_groq_response('Hello from Groq'))
