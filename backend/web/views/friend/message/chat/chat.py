"""AiFriends 聊天接口：JWT → Context → LangGraph/Mock → SSE → optional TTS → Message.

第四轮学习体验改造后的关键点：

* ``AI_MODE=mock``：不访问任何外部模型，也能体验真实 SSE 与数据库链路；
* ``AI_MODE=text``：使用真实 LLM，但默认不要求 RAG/ASR/TTS；
* ``ENABLE_TTS=false``：文本生成不再依赖语音 WebSocket；
* 浏览器取消 SSE 时通过 ``cancel_event`` 尽快停止后台生成；
* 模型名统一来自 ``web.ai.config``。
"""

import asyncio
import base64
import json
import logging
import os
import threading
import uuid
from queue import Queue

import websockets
from django.http import StreamingHttpResponse
from langchain_core.messages import HumanMessage, BaseMessageChunk, SystemMessage, AIMessage
from rest_framework.renderers import BaseRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from web.ai.config import get_ai_settings
from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import CharGraph
from web.views.friend.message.memory.update import update_memory

logger = logging.getLogger(__name__)


class SSERenderer(BaseRenderer):
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def add_system_prompt(state, friend):
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')
    prompt = ''.join(sp.prompt for sp in system_prompts)
    prompt += f'\n[角色性格]\n{friend.character.profile}\n'
    prompt += f'[长期记忆]\n{friend.memory}\n'
    return {'messages': [SystemMessage(prompt)] + msgs}


def add_recent_messages(state, friend):
    msgs = state['messages']
    message_raw = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()
    messages = []
    for item in message_raw:
        messages.append(HumanMessage(item.user_message))
        messages.append(AIMessage(item.output))
    return {'messages': msgs[:1] + messages + msgs[-1:]}


class MessageChatView(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]

    def post(self, request):
        friend_id = request.data.get('friend_id')
        message = (request.data.get('message') or '').strip()

        if not message:
            return Response({'result': '消息不能为空'}, status=400)

        friend = Friend.objects.filter(pk=friend_id, me__user=request.user).first()
        if not friend:
            return Response({'result': '好友不存在'}, status=404)

        inputs = {'messages': [HumanMessage(message)]}
        inputs = add_system_prompt(inputs, friend)
        inputs = add_recent_messages(inputs, friend)
        config = get_ai_settings()

        if config.is_mock:
            iterator = self.mock_event_stream(inputs, friend, message)
        else:
            app = CharGraph.create_app()
            iterator = self.event_stream(app, inputs, friend, message, config)

        response = StreamingHttpResponse(iterator, content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

    def mock_event_stream(self, inputs, friend, message):
        """Deterministic local stream: ideal for Chapter 00–07 with zero API cost."""
        reply = f'【Mock 模式】我收到你的消息：“{message}”。现在你正在练习真实的 Django + JWT + SSE 链路。'
        for start in range(0, len(reply), 6):
            chunk = reply[start:start + 6]
            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"

        self.save_message(friend, message, inputs, reply, {})
        yield 'data: [DONE]\n\n'

    async def text_sender(self, app, inputs, mq, cancel_event):
        """Real LLM streaming without TTS. This is the default path for AI_MODE=text."""
        async for msg, metadata in app.astream(inputs, stream_mode='messages'):
            if cancel_event.is_set():
                break
            if isinstance(msg, BaseMessageChunk):
                if msg.content:
                    mq.put_nowait({'content': msg.content})
                if getattr(msg, 'usage_metadata', None):
                    mq.put_nowait({'usage': msg.usage_metadata})

    async def tts_sender(self, app, inputs, mq, ws, task_id, cancel_event):
        async for msg, metadata in app.astream(inputs, stream_mode='messages'):
            if cancel_event.is_set():
                break
            if isinstance(msg, BaseMessageChunk):
                if msg.content:
                    await ws.send(json.dumps({
                        'header': {
                            'action': 'continue-task',
                            'task_id': task_id,
                            'streaming': 'duplex',
                        },
                        'payload': {'input': {'text': msg.content}},
                    }))
                    mq.put_nowait({'content': msg.content})
                if getattr(msg, 'usage_metadata', None):
                    mq.put_nowait({'usage': msg.usage_metadata})

        await ws.send(json.dumps({
            'header': {
                'action': 'finish-task',
                'task_id': task_id,
                'streaming': 'duplex',
            },
            'payload': {'input': {}},
        }))

    async def tts_receiver(self, mq, ws, cancel_event):
        async for msg in ws:
            if cancel_event.is_set():
                break
            if isinstance(msg, bytes):
                mq.put_nowait({'audio': base64.b64encode(msg).decode('utf8')})
            else:
                data = json.loads(msg)
                if data.get('header', {}).get('event') in ['task-finished', 'task-failed']:
                    break

    async def run_tts_tasks(self, app, inputs, mq, voice_id, cancel_event, tts_model):
        task_id = uuid.uuid4().hex
        headers = {'Authorization': f"Bearer {os.getenv('API_KEY')}"}
        async with websockets.connect(os.getenv('WSS_URL'), additional_headers=headers) as ws:
            await ws.send(json.dumps({
                'header': {
                    'action': 'run-task',
                    'task_id': task_id,
                    'streaming': 'duplex',
                },
                'payload': {
                    'task_group': 'audio',
                    'task': 'tts',
                    'function': 'SpeechSynthesizer',
                    'model': tts_model,
                    'parameters': {
                        'text_type': 'PlainText',
                        'voice': voice_id,
                        'format': 'mp3',
                        'sample_rate': 22050,
                        'volume': 50,
                        'rate': 1.25,
                        'pitch': 1.0,
                    },
                    'input': {},
                },
            }))

            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break

            await asyncio.gather(
                self.tts_sender(app, inputs, mq, ws, task_id, cancel_event),
                self.tts_receiver(mq, ws, cancel_event),
            )

    def work(self, app, inputs, mq, voice_id, cancel_event, config):
        """Bridge async LangGraph/speech code into Django's synchronous SSE generator."""
        try:
            if config.enable_tts and voice_id:
                asyncio.run(self.run_tts_tasks(
                    app, inputs, mq, voice_id, cancel_event, config.tts_model,
                ))
            else:
                asyncio.run(self.text_sender(app, inputs, mq, cancel_event))
        except Exception as exc:
            logger.exception('AI streaming worker failed')
            mq.put_nowait({'error': 'AI 服务调用失败，请查看 Django 日志。'})
        finally:
            mq.put_nowait(None)

    def event_stream(self, app, inputs, friend, message, config):
        mq = Queue()
        cancel_event = threading.Event()
        voice = friend.character.voice
        voice_id = voice.voice_id if voice else None

        thread = threading.Thread(
            target=self.work,
            args=(app, inputs, mq, voice_id, cancel_event, config),
            daemon=True,
        )
        thread.start()

        final_output = ''
        final_usage = {}
        completed = False

        try:
            while True:
                msg = mq.get()
                if msg is None:
                    completed = True
                    break
                if msg.get('content'):
                    final_output += msg['content']
                    yield f"data: {json.dumps({'content': msg['content']}, ensure_ascii=False)}\n\n"
                if msg.get('audio'):
                    yield f"data: {json.dumps({'audio': msg['audio']}, ensure_ascii=False)}\n\n"
                if msg.get('usage'):
                    final_usage = msg['usage']
                if msg.get('error'):
                    yield f"data: {json.dumps({'error': msg['error']}, ensure_ascii=False)}\n\n"
        finally:
            # StreamingHttpResponse is closed when fetch/AbortController disconnects.
            # The worker observes this event and stops feeding more LLM/TTS chunks.
            cancel_event.set()

        if completed:
            # Persistence must happen before [DONE]. A client is allowed to close the
            # stream as soon as it sees the completion marker; saving afterwards made
            # the final message vulnerable to disconnect timing.
            self.save_message(friend, message, inputs, final_output, final_usage)
            yield 'data: [DONE]\n\n'

            if Message.objects.filter(friend=friend).count() % 5 == 0:
                update_memory(friend)

    @staticmethod
    def save_message(friend, message, inputs, output, usage):
        Message.objects.create(
            friend=friend,
            user_message=message[:500],
            input=json.dumps(
                [item.model_dump() for item in inputs['messages']],
                ensure_ascii=False,
            )[:10000],
            output=output[:500],
            input_tokens=usage.get('input_tokens', 0),
            output_tokens=usage.get('output_tokens', 0),
            total_tokens=usage.get('total_tokens', 0),
        )
