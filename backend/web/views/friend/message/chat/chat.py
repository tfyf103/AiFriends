"""
AiFriends 聊天接口的核心入口。

建议零基础同学把这个文件理解成“总调度器”，而不是把它当成单纯的 Django View。

一条用户消息会依次经历：

浏览器 InputField.vue
    -> POST /api/friend/message/chat/
    -> MessageChatView.post()
    -> 拼接系统提示词、角色性格、长期记忆、最近聊天
    -> CharGraph（LangGraph）调用 LLM / Tool
    -> 一边获得模型文本，一边送给 TTS
    -> event_stream() 把文本和音频包装成 SSE
    -> 浏览器实时显示文字并播放声音
    -> 回复结束后写入 Message 数据库
    -> 每 5 条消息压缩一次长期记忆

这个文件同时涉及 Django、DRF、LangChain/LangGraph、SSE、线程、asyncio、WebSocket、TTS。
第一次阅读时不用一次看懂全部，建议先只追踪 post() -> event_stream() 的文字链路，
再回来学习 TTS 部分。
"""

import asyncio
import base64
import json
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

from web.models.friend import Friend, Message, SystemPrompt
from web.views.friend.message.chat.graph import CharGraph
from web.views.friend.message.memory.update import update_memory


class SSERenderer(BaseRenderer):
    """
    告诉 Django REST Framework：这个接口返回的不是普通 JSON，而是 text/event-stream。

    SSE 的数据格式类似：

        data: {"content": "你"}\n\n
        data: {"content": "好"}\n\n
        data: [DONE]\n\n

    两个换行代表一条 SSE 事件结束。
    """
    media_type = 'text/event-stream'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


def add_system_prompt(state, friend):
    """
    给“本轮用户消息”前面插入 SystemMessage。

    SystemPrompt(title='回复')：后台可配置的通用回复规则；
    friend.character.profile：当前 AI 角色的人格设定；
    friend.memory：系统从历史对话中压缩出的长期记忆。

    最终结构大致是：

        SystemMessage(
            通用回复规则
            + 角色性格
            + 长期记忆
        )
        HumanMessage(本轮用户输入)

    LangChain 中 SystemMessage 的优先级通常高于普通 HumanMessage，
    所以角色扮演规则和记忆适合放在这里。
    """
    msgs = state['messages']
    system_prompts = SystemPrompt.objects.filter(title='回复').order_by('order_number')

    prompt = ''
    for sp in system_prompts:
        prompt += sp.prompt

    prompt += f'\n[角色性格]\n{friend.character.profile}\n'
    prompt += f'[长期记忆]\n{friend.memory}\n'

    return {'messages': [SystemMessage(prompt)] + msgs}


def add_recent_messages(state, friend):
    """
    把最近 10 条数据库聊天记录重新转换成 LangChain Message。

    为什么还要“最近聊天”，已经有长期记忆不够吗？

    - 最近聊天：保留原始上下文，细节完整，但不能无限增长；
    - 长期记忆：把较长历史压缩成摘要，占用 token 更少，但会损失细节。

    两者组合，就是这个项目目前的“短期上下文 + 长期记忆”方案。
    """
    msgs = state['messages']

    # 数据库按 id 倒序取最新 10 条，再 reverse() 恢复成从旧到新的对话顺序。
    message_raw = list(Message.objects.filter(friend=friend).order_by('-id')[:10])
    message_raw.reverse()

    messages = []
    for m in message_raw:
        messages.append(HumanMessage(m.user_message))
        messages.append(AIMessage(m.output))

    # msgs[0] 是 SystemMessage，msgs[-1] 是本轮 HumanMessage。
    # 中间插入历史对话，就形成完整上下文。
    return {'messages': msgs[:1] + messages + msgs[-1:]}


class MessageChatView(APIView):
    """处理“给某个 AI 好友发送一条消息”的 API。"""

    # 只有登录用户才能调用。DRF 会先验证 Authorization: Bearer <token>。
    permission_classes = [IsAuthenticated]
    renderer_classes = [SSERenderer]

    def post(self, request):
        """
        HTTP POST 的入口。

        前端请求体：

            {
                "friend_id": 1,
                "message": "你好"
            }

        这里做的事情只有“准备工作”：校验 -> 找好友 -> 构建 LangGraph -> 拼上下文 ->
        返回 StreamingHttpResponse。真正的流式生成发生在 event_stream() 中。
        """
        friend_id = request.data['friend_id']
        message = request.data['message'].strip()

        if not message:
            return Response({
                'result': '消息不能为空',
            })

        # 不仅按主键找 Friend，还限定 me__user=request.user。
        # 这样用户不能随便传一个别人的 friend_id 读取/操作别人的 AI 好友。
        friends = Friend.objects.filter(pk=friend_id, me__user=request.user)
        if not friends.exists():
            return Response({
                'result': '好友不存在',
            })

        friend = friends.first()

        # CharGraph.create_app() 会创建一个 LangGraph：agent <-> tools。
        app = CharGraph.create_app()

        # LangGraph 的状态核心就是 messages。
        inputs = {
            'messages': [HumanMessage(message)],
        }

        # 第一步：加入系统规则、角色性格、长期记忆。
        inputs = add_system_prompt(inputs, friend)

        # 第二步：加入数据库中的最近聊天记录。
        inputs = add_recent_messages(inputs, friend)

        # StreamingHttpResponse 接受一个“可迭代对象/生成器”。
        # event_stream() 每 yield 一次，浏览器就可以尽快收到一段数据，
        # 不必等整个 LLM + TTS 流程全部完成。
        response = StreamingHttpResponse(
            self.event_stream(app, inputs, friend, message),
            content_type="text/event-stream",
        )

        # SSE 常见响应头：禁止缓存；同时告诉 Nginx 不要把流式片段攒在缓冲区后一次性返回。
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'

        return response

    async def tts_sender(self, app, inputs, mq, ws, task_id):
        """
        任务 A：从 LangGraph 获取模型文本流，同时把文本送进 TTS WebSocket。

        数据同时走向两个地方：

        LLM 文本块
          ├─> mq（主线程稍后把它作为 SSE content 发给前端）
          └─> TTS WebSocket（让语音模型开始合成声音）

        这样文字显示和语音合成可以并行进行，而不是“文本全部生成完才开始 TTS”。
        """
        async for msg, metadata in app.astream(inputs, stream_mode="messages"):
            if isinstance(msg, BaseMessageChunk):
                if msg.content:
                    # 将新生成的文字片段持续喂给 TTS 服务。
                    await ws.send(json.dumps({
                        "header": {
                            "action": "continue-task",
                            "task_id": task_id,
                            "streaming": "duplex"
                        },
                        "payload": {
                            "input": {
                                "text": msg.content,
                            }
                        }
                    }))

                    # 同一片文本也进入线程安全 Queue，稍后通过 SSE 发给浏览器。
                    mq.put_nowait({'content': msg.content})

                # 模型供应商在最终 chunk 中可能附带 token 用量。
                if hasattr(msg, 'usage_metadata') and msg.usage_metadata:
                    mq.put_nowait({'usage': msg.usage_metadata})

        # LLM 流结束后，告诉 TTS：“文字已经全部发送完毕，可以结束任务”。
        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            }
        }))

    async def tts_receiver(self, mq, ws):
        """
        任务 B：持续接收 TTS WebSocket 返回的数据。

        - bytes：真正的 MP3 二进制音频；
        - str / JSON：任务状态事件。

        SSE 最终要发送 JSON 文本，因此 bytes 不能直接塞进 JSON，
        这里先 Base64 编码，前端再用 atob() 解码回 Uint8Array。
        """
        async for msg in ws:
            if isinstance(msg, bytes):
                audio = base64.b64encode(msg).decode('utf8')
                mq.put_nowait({'audio': audio})
            else:
                data = json.loads(msg)
                event = data['header']['event']

                if event in ['task-finished', 'task-failed']:
                    break

    async def run_tts_tasks(self, app, inputs, mq, voice_id):
        """
        建立 TTS WebSocket，并并发运行 tts_sender + tts_receiver。

        asyncio.gather() 的意义：
        - sender 不断发送模型生成的新文本；
        - receiver 同时不断接收已经合成出的音频；
        两个协程并行推进，减少语音首包等待时间。
        """
        task_id = uuid.uuid4().hex
        api_key = os.getenv('API_KEY')
        wss_url = os.getenv('WSS_URL')

        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            # 第一次消息用于创建一个 TTS 任务并指定模型、音色和音频格式。
            await ws.send(json.dumps({
                "header": {
                    "action": "run-task",
                    "task_id": task_id,
                    "streaming": "duplex"
                },
                "payload": {
                    "task_group": "audio",
                    "task": "tts",
                    "function": "SpeechSynthesizer",
                    "model": "cosyvoice-v3-flash",
                    "parameters": {
                        "text_type": "PlainText",
                        "voice": voice_id,
                        "format": "mp3",
                        "sample_rate": 22050,
                        "volume": 50,
                        "rate": 1.25,
                        "pitch": 1.0,
                    },
                    "input": {}
                }
            }))

            # 等待服务端确认 task-started 后再真正发送文字。
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break

            await asyncio.gather(
                self.tts_sender(app, inputs, mq, ws, task_id),
                self.tts_receiver(mq, ws),
            )

    def work(self, app, inputs, mq, voice_id):
        """
        在线程中启动 asyncio 事件循环。

        Django 当前的 event_stream() 是同步生成器，但 TTS/LLM 流使用 async API。
        因此这里用一个后台线程运行 asyncio.run()，主线程则阻塞读取 Queue。

        无论成功还是异常，finally 都放入 None 作为“生产结束”哨兵，
        防止 event_stream() 永远等待 mq.get()。
        """
        try:
            asyncio.run(self.run_tts_tasks(app, inputs, mq, voice_id))
        finally:
            mq.put_nowait(None)

    def event_stream(self, app, inputs, friend, message):
        """
        把模型文本 + TTS 音频转换成浏览器能消费的 SSE 流。

        这是理解后端流式响应最关键的方法。
        """
        # Queue 是线程安全的“中转站”：后台线程生产 content/audio，当前生成器消费它们。
        mq = Queue()

        # 当前角色的 voice_id 决定 TTS 使用哪种声音。
        thread = threading.Thread(
            target=self.work,
            args=(app, inputs, mq, friend.character.voice.voice_id),
        )
        thread.start()

        final_output = ''
        final_usage = {}

        while True:
            # mq.get() 在没有数据时会等待；一旦后台线程产生新片段就继续。
            msg = mq.get()

            # None 是 work() 放入的结束哨兵。
            if not msg:
                break

            if msg.get('content', None):
                final_output += msg['content']

                # ensure_ascii=False 让中文保持可读，而不是变成 \u4f60\u597d。
                yield f"data: {json.dumps({'content': msg['content']}, ensure_ascii=False)}\n\n"

            if msg.get('audio', None):
                yield f"data: {json.dumps({'audio': msg['audio']}, ensure_ascii=False)}\n\n"

            if msg.get('usage', None):
                final_usage = msg['usage']

        # 自定义结束标记。前端 streamApi.js 遇到它后会把 isDone 设为 true。
        yield "data: [DONE]\n\n"

        # 流结束后再统一保存完整回复和 token 统计。
        input_tokens = final_usage.get('input_tokens', 0)
        output_tokens = final_usage.get('output_tokens', 0)
        total_tokens = final_usage.get('total_tokens', 0)

        Message.objects.create(
            friend=friend,
            user_message=message[:500],

            # 保存实际发送给模型的 messages，便于开发阶段调试提示词和上下文。
            input=json.dumps(
                [m.model_dump() for m in inputs['messages']],
                ensure_ascii=False,
            )[:10000],

            output=final_output[:500],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
        )

        # 当前策略：每产生 5 条 Message，就重新压缩一次长期记忆。
        # 这样不用每轮都额外调用一次记忆模型，也不会让长期记忆太久不更新。
        if Message.objects.filter(friend=friend).count() % 5 == 0:
            update_memory(friend)
