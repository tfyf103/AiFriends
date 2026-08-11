import os
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from web.ai.config import get_ai_settings
from web.models.character import Character, Voice
from web.models.friend import Friend, Message
from web.models.user import UserProfile


class AIConfigTests(TestCase):
    def test_mock_mode_needs_no_optional_features(self):
        with patch.dict(os.environ, {'AI_MODE': 'mock'}, clear=False):
            for name in ['ENABLE_RAG', 'ENABLE_ASR', 'ENABLE_TTS']:
                os.environ.pop(name, None)
            config = get_ai_settings()
            self.assertTrue(config.is_mock)
            self.assertFalse(config.enable_rag)
            self.assertFalse(config.enable_asr)
            self.assertFalse(config.enable_tts)

    def test_full_mode_keeps_old_feature_defaults(self):
        with patch.dict(os.environ, {'AI_MODE': 'full'}, clear=False):
            for name in ['ENABLE_RAG', 'ENABLE_ASR', 'ENABLE_TTS']:
                os.environ.pop(name, None)
            config = get_ai_settings()
            self.assertTrue(config.enable_rag)
            self.assertTrue(config.enable_asr)
            self.assertTrue(config.enable_tts)


@override_settings(DEBUG=True)
class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_hashes_password_and_sets_dev_cookie(self):
        response = self.client.post('/api/user/account/register/', {
            'username': 'alice',
            'password': 'secret123',
        }, format='json')

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='alice')
        self.assertTrue(user.check_password('secret123'))
        self.assertNotEqual(user.password, 'secret123')
        self.assertIn('refresh_token', response.cookies)
        self.assertFalse(response.cookies['refresh_token']['secure'])

    def test_duplicate_username_returns_conflict(self):
        User.objects.create_user(username='alice', password='secret123')
        response = self.client.post('/api/user/account/register/', {
            'username': 'alice',
            'password': 'other123',
        }, format='json')
        self.assertEqual(response.status_code, 409)

    def test_wrong_password_returns_401(self):
        user = User.objects.create_user(username='alice', password='secret123')
        UserProfile.objects.create(user=user)
        response = self.client.post('/api/user/account/login/', {
            'username': 'alice',
            'password': 'wrong',
        }, format='json')
        self.assertEqual(response.status_code, 401)

    def test_refresh_cookie_returns_new_access(self):
        register = self.client.post('/api/user/account/register/', {
            'username': 'alice',
            'password': 'secret123',
        }, format='json')
        self.client.cookies['refresh_token'] = register.cookies['refresh_token'].value
        refresh = self.client.post('/api/user/account/refresh_token/', {}, format='json')
        self.assertEqual(refresh.status_code, 200)
        self.assertTrue(refresh.data['access'])
        self.assertIn('refresh_token', refresh.cookies)


class MockChatTests(TestCase):
    def setUp(self):
        self.tmp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.tmp_media.name)
        self.media_override.enable()

        self.user = User.objects.create_user(username='learner', password='secret123')
        profile = UserProfile.objects.create(user=self.user)
        voice = Voice.objects.create(name='Demo', voice_id='demo-voice')
        self.character = Character.objects.create(
            author=profile,
            name='Nova',
            photo=SimpleUploadedFile('photo.jpg', b'fake-image'),
            voice=voice,
            profile='A friendly teaching assistant.',
            background_image=SimpleUploadedFile('background.jpg', b'fake-image'),
        )
        self.friend = Friend.objects.create(me=profile, character=self.character)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.media_override.disable()
        self.tmp_media.cleanup()

    def test_mock_chat_streams_and_persists_without_external_api(self):
        with patch.dict(os.environ, {
            'AI_MODE': 'mock',
            'ENABLE_RAG': 'false',
            'ENABLE_ASR': 'false',
            'ENABLE_TTS': 'false',
        }, clear=False):
            response = self.client.post('/api/friend/message/chat/', {
                'friend_id': self.friend.id,
                'message': '你好',
            }, format='json')
            body = b''.join(response.streaming_content).decode('utf8')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text/event-stream', response['Content-Type'])
        self.assertIn('Mock', body)
        self.assertIn('[DONE]', body)
        self.assertEqual(Message.objects.filter(friend=self.friend).count(), 1)

    def test_asr_disabled_returns_clear_503(self):
        with patch.dict(os.environ, {'AI_MODE': 'text', 'ENABLE_ASR': 'false'}, clear=False):
            response = self.client.post('/api/friend/message/asr/asr/', {})
        self.assertEqual(response.status_code, 503)
        self.assertIn('ASR 未启用', response.data['result'])
