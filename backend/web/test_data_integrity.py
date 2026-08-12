import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from web.models.character import Character, Voice
from web.models.user import UserProfile


class CharacterVoiceIntegrityTests(TestCase):
    def test_removing_voice_does_not_delete_character(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            user = User.objects.create_user(username='voice-owner', password='secret123')
            profile = UserProfile.objects.create(user=user)
            voice = Voice.objects.create(name='Retired voice', voice_id='retired-voice')
            character = Character.objects.create(
                author=profile,
                name='Keep me',
                photo=SimpleUploadedFile('photo.jpg', b'legacy-test-image'),
                voice=voice,
                profile='Character data must survive provider configuration changes.',
                background_image=SimpleUploadedFile('background.jpg', b'legacy-test-image'),
            )

            voice.delete()
            character.refresh_from_db()

            self.assertIsNone(character.voice_id)
            self.assertEqual(character.name, 'Keep me')
