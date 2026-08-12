import os
import tempfile
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from web.models.character import Character, Voice
from web.models.friend import Friend, Message
from web.models.user import UserProfile


class ChatCompletionPersistenceTests(TestCase):
    def setUp(self):
        self.tmp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.tmp_media.name)
        self.media_override.enable()

        user = User.objects.create_user(username='stream-user', password='secret123')
        profile = UserProfile.objects.create(user=user)
        voice = Voice.objects.create(name='Demo', voice_id='demo-voice')
        character = Character.objects.create(
            author=profile,
            name='Nova',
            photo=SimpleUploadedFile('photo.jpg', b'legacy-test-image'),
            voice=voice,
            profile='A friendly teaching assistant.',
            background_image=SimpleUploadedFile('background.jpg', b'legacy-test-image'),
        )
        self.friend = Friend.objects.create(me=profile, character=character)
        self.client = APIClient()
        self.client.force_authenticate(user)

    def tearDown(self):
        self.media_override.disable()
        self.tmp_media.cleanup()

    def test_message_exists_when_done_event_is_observed(self):
        with patch.dict(os.environ, {
            'AI_MODE': 'mock',
            'ENABLE_RAG': 'false',
            'ENABLE_ASR': 'false',
            'ENABLE_TTS': 'false',
        }, clear=False):
            response = self.client.post('/api/friend/message/chat/', {
                'friend_id': self.friend.id,
                'message': '请记住这条消息',
            }, format='json')

            saw_done = False
            for chunk in response.streaming_content:
                if b'[DONE]' in chunk:
                    saw_done = True
                    self.assertEqual(Message.objects.filter(friend=self.friend).count(), 1)
                    break
            response.close()

        self.assertTrue(saw_done)
