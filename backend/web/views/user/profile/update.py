import logging

from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile
from web.views.utils.photo import remove_old_photos
from web.views.utils.uploads import ImageUploadError, validate_image_upload

logger = logging.getLogger(__name__)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user_profile = UserProfile.objects.filter(user=user).first()
        if not user_profile:
            return Response({
                'result': '当前账户缺少 UserProfile',
                'code': 'USER_PROFILE_MISSING',
            }, status=409)

        username = (request.data.get('username') or '').strip()[:150]
        profile = (request.data.get('profile') or '').strip()[:500]
        photo = request.FILES.get('photo')

        if not username:
            return Response({'result': '用户名不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if not profile:
            return Response({'result': '简介不能为空', 'code': 'VALIDATION_ERROR'}, status=400)
        if username != user.username and User.objects.filter(username=username).exists():
            return Response({'result': '用户名已存在', 'code': 'USERNAME_EXISTS'}, status=409)

        try:
            if photo:
                validate_image_upload(photo)
        except ImageUploadError as exc:
            return Response({'result': str(exc), 'code': 'INVALID_IMAGE'}, status=400)

        old_photo = user_profile.photo if photo else None
        if photo:
            user_profile.photo = photo
        user_profile.profile = profile
        user_profile.update_time = now()
        user.username = username

        try:
            user.save(update_fields=['username'])
            user_profile.save()
        except Exception:
            logger.exception('Profile update failed for user_id=%s', user.id)
            return Response({
                'result': '系统异常，请稍后重试',
                'code': 'PROFILE_UPDATE_FAILED',
            }, status=500)

        if old_photo:
            remove_old_photos(old_photo)

        return Response({
            'result': 'success',
            'user_id': user.id,
            'username': user.username,
            'profile': user_profile.profile,
            'photo': user_profile.photo.url,
        })
