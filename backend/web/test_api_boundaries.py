import os
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile


class APIBoundaryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='api-user', password='secret123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.character = Character.objects.create(
            author=self.profile,
            name='No voice needed',
            photo=SimpleUploadedFile('photo.jpg', b'legacy-test-image'),
            voice=None,
            profile='Boundary test character.',
            background_image=SimpleUploadedFile('background.jpg', b'legacy-test-image'),
        )
        self.friend = Friend.objects.create(me=self.profile, character=self.character)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_history_rejects_invalid_cursor(self):
        response = self.client.get('/api/friend/message/get_history/', {
            'friend_id': self.friend.id,
            'last_message_id': 'not-an-int',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], 'VALIDATION_ERROR')

    def test_history_rejects_unknown_friend(self):
        response = self.client.get('/api/friend/message/get_history/', {
            'friend_id': 999999,
            'last_message_id': 0,
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['code'], 'FRIEND_NOT_FOUND')

    def test_remove_friend_rejects_unknown_friend(self):
        response = self.client.post('/api/friend/remove/', {
            'friend_id': 999999,
        }, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['code'], 'FRIEND_NOT_FOUND')

    def test_asr_rejects_large_audio_before_provider_call(self):
        large_pcm = SimpleUploadedFile(
            'voice.pcm',
            b'0' * (5 * 1024 * 1024 + 1),
            content_type='audio/pcm',
        )
        with patch.dict(os.environ, {
            'AI_MODE': 'text',
            'ENABLE_ASR': 'true',
        }, clear=False):
            response = self.client.post('/api/friend/message/asr/asr/', {
                'audio': large_pcm,
            }, format='multipart')
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.data['code'], 'AUDIO_TOO_LARGE')
