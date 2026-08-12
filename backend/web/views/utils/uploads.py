"""Security-oriented validation for user-supplied image uploads."""

from pathlib import Path

from PIL import Image, UnidentifiedImageError


MAX_IMAGE_BYTES = 8 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000
ALLOWED_IMAGE_FORMATS = {
    'JPEG': 'jpg',
    'PNG': 'png',
    'WEBP': 'webp',
}


class ImageUploadError(ValueError):
    pass


def validate_image_upload(upload, *, max_bytes=MAX_IMAGE_BYTES):
    """Validate image bytes and normalize the extension used by ImageField storage.

    The previous views trusted the browser filename and accepted arbitrary bytes. That
    could store non-images under MEDIA_URL and also allowed very large uploads. Pillow
    verifies the payload, the pixel cap limits decompression bombs, and the normalized
    extension prevents a valid image from being stored with an HTML/SVG-like suffix.
    """
    if upload is None:
        return None

    if upload.size <= 0:
        raise ImageUploadError('图片文件为空')
    if upload.size > max_bytes:
        raise ImageUploadError(f'图片不能超过 {max_bytes // (1024 * 1024)} MB')

    try:
        image = Image.open(upload)
        image_format = image.format
        width, height = image.size
        if width <= 0 or height <= 0 or width * height > MAX_IMAGE_PIXELS:
            raise ImageUploadError('图片尺寸过大或无效')
        image.verify()
    except ImageUploadError:
        raise
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError, ValueError) as exc:
        raise ImageUploadError('只支持有效且尺寸安全的 JPEG、PNG 或 WebP 图片') from exc
    finally:
        upload.seek(0)

    extension = ALLOWED_IMAGE_FORMATS.get(image_format)
    if not extension:
        raise ImageUploadError('只支持 JPEG、PNG 或 WebP 图片')

    stem = Path(upload.name or 'image').stem[:40] or 'image'
    upload.name = f'{stem}.{extension}'
    return upload
