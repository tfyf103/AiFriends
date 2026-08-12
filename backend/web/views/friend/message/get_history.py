from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.friend import Friend, Message


class GetHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friend_id = request.query_params.get('friend_id')
        if not friend_id:
            return Response({
                'result': 'friend_id 不能为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        try:
            last_message_id = int(request.query_params.get('last_message_id', 0))
        except (TypeError, ValueError):
            return Response({
                'result': 'last_message_id 必须是整数',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        if last_message_id < 0:
            return Response({
                'result': 'last_message_id 不能为负数',
                'code': 'VALIDATION_ERROR',
            }, status=400)

        friend = Friend.objects.filter(id=friend_id, me__user=request.user).first()
        if not friend:
            return Response({
                'result': '好友不存在',
                'code': 'FRIEND_NOT_FOUND',
            }, status=404)

        queryset = Message.objects.filter(friend=friend)
        if last_message_id > 0:
            queryset = queryset.filter(pk__lt=last_message_id)

        messages = [
            {
                'id': message.id,
                'user_message': message.user_message,
                'output': message.output,
            }
            for message in queryset.order_by('-id')[:10]
        ]
        return Response({
            'result': 'success',
            'messages': messages,
        })
