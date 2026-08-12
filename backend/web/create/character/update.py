import logging

from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character, Voice
from web.views.utils.photo import remove_old_photos
from web.views.utils.uploads import ImageUploadError, validate_image_upload

logger = logging.getLogger(__name__)


class UpdateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        character_id = request.data.get('character_id')
        character = Character.objects.filter(
            id=character_id,
            author__user=request.user,
        ).first()
        if not character:
            return Response({
                'result': '角色不存在或无权修改',
                'code': 'CHARACTER_NOT_FOUND',
            }, status=404)

        name = (request.data.get('name') or '').strip()[:50]
        profile = (request.data.get('profile') or '').strip()[:100000]
        voice_id = request.data.get('voice_id')
        photo = request.FILES.get('photo')
        background_image = request.FILES.get('background_image')

        if not name:
            return Response({'result': '名字不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if not profile:
            return Response({'result': '角色简介不能为空', 'code': 'VALIDATION_ERROR'}, status=400)

        voice = Voice.objects.filter(id=voice_id).first()
        if not voice:
            return Response({'result': '音色不存在', 'code': 'VOICE_NOT_FOUND'}, status=400)

        try:
            if photo:
                validate_image_upload(photo)
            if background_image:
                validate_image_upload(background_image)
        except ImageUploadError as exc:
            return Response({
                'result': str(exc),
                'code': 'INVALID_IMAGE',
            }, status=400)

        old_photo = character.photo if photo else None
        old_background = character.background_image if background_image else None

        if photo:
            character.photo = photo
        if background_image:
            character.background_image = background_image
        character.name = name
        character.voice = voice
        character.profile = profile
        character.update_time = now()

        try:
            character.save()
        except Exception:
            logger.exception('Character update failed for character_id=%s', character.id)
            return Response({
                'result': '更新角色异常，请稍后重试',
                'code': 'CHARACTER_UPDATE_FAILED',
            }, status=500)

        # Only remove old files after the database/storage save succeeds. The old
        # implementation deleted them first, so a later save failure could lose data.
        if old_photo:
            remove_old_photos(old_photo)
        if old_background:
            remove_old_photos(old_background)

        return Response({'result': 'success'})
