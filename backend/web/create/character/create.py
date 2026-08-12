import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character, Voice
from web.models.user import UserProfile
from web.views.utils.uploads import ImageUploadError, validate_image_upload

logger = logging.getLogger(__name__)


class CreateCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            return Response({
                'result': '当前账户缺少 UserProfile',
                'code': 'USER_PROFILE_MISSING',
            }, status=409)

        name = (request.data.get('name') or '').strip()[:50]
        profile = (request.data.get('profile') or '').strip()[:100000]
        voice_id = request.data.get('voice_id')
        photo = request.FILES.get('photo')
        background_image = request.FILES.get('background_image')

        if not name:
            return Response({'result': '名字不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if not profile:
            return Response({'result': '角色简介不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if not photo:
            return Response({'result': '头像不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if not background_image:
            return Response({'result': '聊天背景不能为空', 'code': 'VALIDATION_ERROR'}, status=400)

        voice = Voice.objects.filter(id=voice_id).first()
        if not voice:
            return Response({'result': '音色不存在', 'code': 'VOICE_NOT_FOUND'}, status=400)

        try:
            validate_image_upload(photo)
            validate_image_upload(background_image)
        except ImageUploadError as exc:
            return Response({
                'result': str(exc),
                'code': 'INVALID_IMAGE',
            }, status=400)

        try:
            character = Character.objects.create(
                author=user_profile,
                name=name,
                voice=voice,
                profile=profile,
                photo=photo,
                background_image=background_image,
            )
        except Exception:
            logger.exception('Character creation failed for user_id=%s', request.user.id)
            return Response({
                'result': '创建角色异常，请稍后重试',
                'code': 'CHARACTER_CREATE_FAILED',
            }, status=500)

        return Response({
            'result': 'success',
            'character_id': character.id,
        }, status=201)
