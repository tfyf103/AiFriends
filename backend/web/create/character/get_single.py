from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character, Voice


class GetSingleCharacterView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        character_id = request.query_params.get('character_id')
        if not character_id:
            return Response({
                'result': 'character_id 不能为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        character = Character.objects.filter(
            id=character_id,
            author__user=request.user,
        ).select_related('voice').first()
        if not character:
            return Response({
                'result': '角色不存在或无权修改',
                'code': 'CHARACTER_NOT_FOUND',
            }, status=404)

        voices = [
            {'id': voice.id, 'name': voice.name}
            for voice in Voice.objects.order_by('id')
        ]

        return Response({
            'result': 'success',
            'character': {
                'id': character.id,
                'name': character.name,
                'profile': character.profile,
                'photo': character.photo.url,
                'background_image': character.background_image.url,
                'voice_id': character.voice_id,
            },
            'voices': voices,
        })
