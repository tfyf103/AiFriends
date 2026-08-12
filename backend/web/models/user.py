import io
import uuid

from PIL import Image, ImageDraw
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.utils.timezone import localtime, now


DEFAULT_USER_PHOTO = 'user/photos/default.png'


def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'user/photos/{instance.user_id}_{filename}'


def ensure_default_user_photo(storage):
    """Create the default avatar in the active MEDIA storage when it is missing.

    MEDIA_ROOT is intentionally configurable (tests use a fresh temporary directory),
    so a repository-local image alone cannot guarantee that `/media/.../default.png`
    exists. Generating a tiny PNG through Django's storage API keeps every deployment
    and test environment self-contained.
    """
    if storage.exists(DEFAULT_USER_PHOTO):
        return

    image = Image.new('RGB', (256, 256), '#e5e7eb')
    draw = ImageDraw.Draw(image)
    draw.ellipse((78, 42, 178, 142), fill='#9ca3af')
    draw.ellipse((48, 132, 208, 292), fill='#9ca3af')

    buffer = io.BytesIO()
    image.save(buffer, format='PNG', optimize=True)
    storage.save(DEFAULT_USER_PHOTO, ContentFile(buffer.getvalue()))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default=DEFAULT_USER_PHOTO, upload_to=photo_upload_to)
    profile = models.TextField(default='谢谢你的关注', max_length=500)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.photo or self.photo.name == DEFAULT_USER_PHOTO:
            ensure_default_user_photo(self._meta.get_field('photo').storage)
        super().save(*args, **kwargs)

    def __str__(self):
        created = localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
        return f'{self.user.username} Profile - {created}'
