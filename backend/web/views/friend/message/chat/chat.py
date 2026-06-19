import json

from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk
from rest_framework import response
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.models.friend import Friend
from web.views.friend.message.chat.graph import CharGraph

class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]
    def post(self, request):
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()
        if not message:
            return Response({
                'result': '消息不能为空',
            })
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': '好友不存在',
            })
        friend = friends.first()
        app = CharGraph.create_app()

        inputs = {
            'messages': [HumanMessage(message)],
        }

        def event_stream():
            final_usage = {}
            for msg, metadata in app.stream(inputs, stream_mode="messages"):
                if isinstance(msg, BaseMessageChunk):
                    if msg.content:
                        yield f"data: {json.dumps({'content': msg.content}, ensure_ascii=False)}\n\n"
                    if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                        final_usage = msg.usage_metadata
            yield "data: [DONE]\n\n"
            print(final_usage)

        response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response