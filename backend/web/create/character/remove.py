from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character
from web.views.utils.photo import remove_old_photos


class RemoveCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        character_id = request.data.get('character_id')
        if not character_id:
            return Response({
                'result': 'character_id 不能为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        character = Character.objects.filter(
            pk=character_id,
            author__user=request.user,
        ).first()
        if not character:
            return Response({
                'result': '角色不存在或无权删除',
                'code': 'CHARACTER_NOT_FOUND',
            }, status=404)

        photo = character.photo
        background_image = character.background_image
        character.delete()
        remove_old_photos(photo)
        remove_old_photos(background_image)
        return Response({'result': 'success'})
