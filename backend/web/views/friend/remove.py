from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.friend import Friend


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        friend_id = request.data.get('friend_id')
        if not friend_id:
            return Response({
                'result': 'friend_id 不能为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        friend = Friend.objects.filter(id=friend_id, me__user=request.user).first()
        if not friend:
            return Response({
                'result': '好友不存在',
                'code': 'FRIEND_NOT_FOUND',
            }, status=404)

        friend.delete()
        return Response({'result': 'success'})
