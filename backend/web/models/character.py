import uuid

from django.db import models
from django.utils.timezone import localtime, now

from web.models.user import UserProfile


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'photos/photos/{instance.author.user_id}_{filename}'


def background_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'photos/background_images/{instance.author.user_id}_{filename}'


class Voice(models.Model):
    name = models.CharField(max_length=100)
    voice_id = models.CharField(max_length=100)
    create_time = models.DateTimeField(default=now)

    def __str__(self):
        created = localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.name} - {self.voice_id} - {created}'


class Character(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to=photo_upload_to)
    # Voice is optional runtime configuration. Removing a provider voice must not
    # cascade-delete user-authored Characters and their Friend/Message history.
    voice = models.ForeignKey(
        Voice,
        default=None,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    profile = models.TextField(max_length=100000)
    background_image = models.ImageField(upload_to=background_image_upload_to)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        created = localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.author.user.username} - {self.name} - {created}'
