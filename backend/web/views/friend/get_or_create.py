from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.character import Character
from web.models.friend import Friend
from web.models.user import UserProfile


class GetOrCreateFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        character_id = request.data.get('character_id')
        if not character_id:
            return Response({
                'result': 'character_id 不能为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        character = (
            Character.objects
            .select_related('author__user')
            .filter(pk=character_id)
            .first()
        )
        if not character:
            return Response({
                'result': '角色不存在',
                'code': 'CHARACTER_NOT_FOUND',
            }, status=404)

        user_profile = UserProfile.objects.filter(user=request.user).first()
        if not user_profile:
            return Response({
                'result': '当前账户缺少 UserProfile',
                'code': 'USER_PROFILE_MISSING',
            }, status=409)

        # get_or_create gives the View a concise API, while the database-level
        # UniqueConstraint is the final concurrency-safe invariant.
        friend, created = Friend.objects.get_or_create(
            character=character,
            me=user_profile,
        )

        author = character.author
        return Response({
            'result': 'success',
            'created': created,
            'friend': {
                'id': friend.id,
                'character': {
                    'id': character.id,
                    'name': character.name,
                    'profile': character.profile,
                    'photo': character.photo.url,
                    'background_image': character.background_image.url,
                    'author': {
                        'user_id': author.user_id,
                        'username': author.user.username,
                        'photo': author.photo.url,
                    },
                },
            },
        }, status=201 if created else 200)
