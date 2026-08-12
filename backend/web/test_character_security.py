import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from web.models.character import Character, Voice
from web.models.user import UserProfile


class CharacterSecurityTests(TestCase):
    def setUp(self):
        self.tmp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.tmp_media.name)
        self.media_override.enable()

        self.owner = User.objects.create_user(username='owner', password='secret123')
        self.owner_profile = UserProfile.objects.create(user=self.owner)
        self.other = User.objects.create_user(username='other', password='secret123')
        self.other_profile = UserProfile.objects.create(user=self.other)
        self.voice = Voice.objects.create(name='Demo', voice_id='demo-voice')
        self.character = Character.objects.create(
            author=self.owner_profile,
            name='Private edit target',
            photo=SimpleUploadedFile('photo.jpg', b'legacy-test-image'),
            voice=self.voice,
            profile='Owned by another user.',
            background_image=SimpleUploadedFile('background.jpg', b'legacy-test-image'),
        )

        self.client = APIClient()
        self.client.force_authenticate(self.other)

    def tearDown(self):
        self.media_override.disable()
        self.tmp_media.cleanup()

    def test_other_user_cannot_read_character_edit_payload(self):
        response = self.client.get('/api/create/character/get_single/', {
            'character_id': self.character.id,
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['code'], 'CHARACTER_NOT_FOUND')

    def test_other_user_cannot_update_character(self):
        response = self.client.post('/api/create/character/update/', {
            'character_id': self.character.id,
            'name': 'stolen',
            'voice_id': self.voice.id,
            'profile': 'stolen',
        }, format='multipart')
        self.assertEqual(response.status_code, 404)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, 'Private edit target')

    def test_other_user_cannot_delete_character(self):
        response = self.client.post('/api/create/character/remove/', {
            'character_id': self.character.id,
        }, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Character.objects.filter(pk=self.character.id).exists())

    def test_character_create_rejects_non_image_uploads(self):
        response = self.client.post('/api/create/character/create/', {
            'name': 'Unsafe upload',
            'voice_id': self.voice.id,
            'profile': 'Should be rejected before storage.',
            'photo': SimpleUploadedFile('avatar.html', b'<script>alert(1)</script>', content_type='text/html'),
            'background_image': SimpleUploadedFile('bg.png', b'not-a-real-image', content_type='image/png'),
        }, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], 'INVALID_IMAGE')

    def test_profile_update_rejects_non_image_upload(self):
        response = self.client.post('/api/user/profile/update/', {
            'username': self.other.username,
            'profile': 'still safe',
            'photo': SimpleUploadedFile('avatar.svg', b'<svg onload="alert(1)"/>', content_type='image/svg+xml'),
        }, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['code'], 'INVALID_IMAGE')
