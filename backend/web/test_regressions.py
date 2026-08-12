import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from web.models.user import DEFAULT_USER_PHOTO, UserProfile


@override_settings(DEBUG=True)
class RefreshTokenRevocationTests(TestCase):
    def setUp(self):
        self.tmp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.tmp_media.name)
        self.media_override.enable()
        self.client = APIClient()

    def tearDown(self):
        self.media_override.disable()
        self.tmp_media.cleanup()

    def register(self, username='security-user'):
        return self.client.post('/api/user/account/register/', {
            'username': username,
            'password': 'security-password-123',
        }, format='json')

    def test_rotated_refresh_token_cannot_be_reused(self):
        register = self.register()
        self.assertEqual(register.status_code, 201)
        old_refresh = register.cookies['refresh_token'].value

        self.client.cookies['refresh_token'] = old_refresh
        rotated = self.client.post('/api/user/account/refresh_token/', {}, format='json')
        self.assertEqual(rotated.status_code, 200)
        self.assertNotEqual(rotated.cookies['refresh_token'].value, old_refresh)

        self.client.cookies['refresh_token'] = old_refresh
        replay = self.client.post('/api/user/account/refresh_token/', {}, format='json')
        self.assertEqual(replay.status_code, 401)
        self.assertEqual(replay.data['code'], 'REFRESH_TOKEN_INVALID')

    def test_logout_revokes_refresh_token_not_only_cookie(self):
        register = self.register('logout-user')
        refresh = register.cookies['refresh_token'].value
        access = register.data['access']

        self.client.cookies['refresh_token'] = refresh
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        logout = self.client.post('/api/user/account/logout/', {}, format='json')
        self.assertEqual(logout.status_code, 200)

        self.client.credentials()
        self.client.cookies['refresh_token'] = refresh
        replay = self.client.post('/api/user/account/refresh_token/', {}, format='json')
        self.assertEqual(replay.status_code, 401)
        self.assertEqual(replay.data['code'], 'REFRESH_TOKEN_INVALID')


class DefaultAvatarTests(TestCase):
    def test_profile_creation_provisions_default_avatar_in_active_storage(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            user = User.objects.create_user(username='avatar-user', password='secret123')
            profile = UserProfile.objects.create(user=user)
            storage = UserProfile._meta.get_field('photo').storage

            self.assertEqual(profile.photo.name, DEFAULT_USER_PHOTO)
            self.assertTrue(storage.exists(DEFAULT_USER_PHOTO))

            with storage.open(DEFAULT_USER_PHOTO, 'rb') as avatar:
                self.assertEqual(avatar.read(8), b'\x89PNG\r\n\x1a\n')
