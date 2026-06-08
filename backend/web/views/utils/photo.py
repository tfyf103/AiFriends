import os
from pathlib import Path
from django.conf import settings


def remove_old_photos(photo):
    # 1. 安全判断：photo对象存在，且不是默认头像
    if not photo or not photo.name:
        return
    if photo.name == 'user/photos/default.png':
        return

    try:
        # 2. 用Path对象拼接，自动适配Windows/Linux路径分隔符
        media_root = Path(settings.MEDIA_ROOT)
        old_path = media_root / photo.name

        # 3. 正确调用exists()，不带参数
        if old_path.exists() and old_path.is_file():
            os.remove(old_path)
    except Exception as e:
        # 只打警告日志，不抛异常，不影响主流程
        print(f"警告：删除旧头像失败 - {str(e)}")