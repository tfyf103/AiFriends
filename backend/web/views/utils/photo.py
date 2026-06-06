import os

from django.conf import settings

def remove_old_photos(photo):
    if photo and photo.name != 'user/photos/default.png':
        old_path = settings.MEDIA_ROOT / photo.name
        if old_path.exists(old_path):
            os.remove(old_path)