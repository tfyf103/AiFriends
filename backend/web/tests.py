import os
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import TestCase, override_settings
from langchain_core.documents import Document
from rest_framework.test import APIClient

from web.ai.config import get_ai_settings
from web.documents.retrieval import document_source
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

    def test_register_serializer_returns_field_errors(self):
        response = self.client.post('/api/user/account/register/', {
            'username': 'alice',
            'password': '123',
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], 'VALIDATION_ERROR')
        self.assertIn('password', response.data['errors'])

    def test_duplicate_username_returns_conflict(self):
        User.objects.create_user(username='alice', password='secret123')
        response = self.client.post('/api/user/account/register/', {
            'username': 'alice',
            'password': 'other123',
        }, format='json')
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['code'], 'USERNAME_EXISTS')

    def test_wrong_password_returns_401(self):
        user = User.objects.create_user(username='alice', password='secret123')
        UserProfile.objects.create(user=user)
        response = self.client.post('/api/user/account/login/', {
            'username': 'alice',
            'password': 'wrong',
        }, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['code'], 'AUTH_INVALID_CREDENTIALS')

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


class HealthTests(TestCase):
    def test_health_is_public_and_has_request_id(self):
        with patch.dict(os.environ, {'AI_MODE': 'mock'}, clear=False):
            response = APIClient().get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'ok')
        self.assertEqual(response.data['ai_mode'], 'mock')
        self.assertTrue(response['X-Request-ID'])
        self.assertEqual(response.data['request_id'], response['X-Request-ID'])

    def test_client_request_id_is_preserved(self):
        response = APIClient().get('/api/health/', HTTP_X_REQUEST_ID='learn-123')
        self.assertEqual(response['X-Request-ID'], 'learn-123')
        self.assertEqual(response.data['request_id'], 'learn-123')


class RAGUtilityTests(TestCase):
    def test_document_source_does_not_leak_absolute_path(self):
        document = Document(
            page_content='example',
            metadata={'source': '/srv/private/aifriends/data.txt'},
        )
        self.assertEqual(document_source(document), 'data.txt')


class MockChatTests(TestCase):
    def setUp(self):
        self.tmp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.tmp_media.name)
        self.media_override.enable()

        self.user = User.objects.create_user(username='learner', password='secret123')
        self.profile = UserProfile.objects.create(user=self.user)
        voice = Voice.objects.create(name='Demo', voice_id='demo-voice')
        self.character = Character.objects.create(
            author=self.profile,
            name='Nova',
            photo=SimpleUploadedFile('photo.jpg', b'fake-image'),
            voice=voice,
            profile='A friendly teaching assistant.',
            background_image=SimpleUploadedFile('background.jpg', b'fake-image'),
        )
        self.friend = Friend.objects.create(me=self.profile, character=self.character)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.media_override.disable()
        self.tmp_media.cleanup()

    def test_friend_database_constraint_exists(self):
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(
                cursor,
                Friend._meta.db_table,
            )
        self.assertIn('unique_friend_per_user_character', constraints)
        self.assertTrue(constraints['unique_friend_per_user_character']['unique'])

    def test_friend_get_or_create_is_idempotent(self):
        response = self.client.post('/api/friend/get_or_create/', {
            'character_id': self.character.id,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data['created'])
        self.assertEqual(response.data['friend']['id'], self.friend.id)
        self.assertEqual(
            Friend.objects.filter(me=self.profile, character=self.character).count(),
            1,
        )

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
