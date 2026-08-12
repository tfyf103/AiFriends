import asyncio
import json
import logging
import os
import uuid

import websockets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.ai.config import get_ai_settings

logger = logging.getLogger(__name__)
MAX_ASR_BYTES = 5 * 1024 * 1024


class ASRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        config = get_ai_settings()
        if not config.enable_asr:
            return Response({
                'result': 'ASR 未启用。请在 .env 中设置 ENABLE_ASR=true。',
            }, status=503)

        audio = request.FILES.get('audio')
        if not audio:
            return Response({
                'result': '音频不存在',
                'code': 'VALIDATION_ERROR',
            }, status=400)
        if audio.size <= 0:
            return Response({
                'result': '音频为空',
                'code': 'VALIDATION_ERROR',
            }, status=400)
        if audio.size > MAX_ASR_BYTES:
            return Response({
                'result': '音频不能超过 5 MB',
                'code': 'AUDIO_TOO_LARGE',
            }, status=413)

        pcm_data = audio.read()
        try:
            text = asyncio.run(self.run_asr_tasks(pcm_data, config.asr_model))
        except Exception:
            logger.exception('ASR provider request failed')
            return Response({
                'result': 'ASR 服务调用失败，请稍后重试',
                'code': 'ASR_PROVIDER_FAILED',
            }, status=502)
        return Response({'result': 'success', 'text': text})

    async def asr_sender(self, pcm_data, ws, task_id):
        chunk = 3200
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i + chunk])
            await asyncio.sleep(0.01)
        await ws.send(json.dumps({
            'header': {
                'action': 'finish-task',
                'task_id': task_id,
                'streaming': 'duplex',
            },
            'payload': {'input': {}},
        }))

    async def asr_receiver(self, ws):
        text = ''
        async for msg in ws:
            data = json.loads(msg)
            event = data['header']['event']
            if event == 'result-generated':
                output = data['payload']['output']
                transcription = output.get('transcription')
                if transcription and transcription.get('sentence_end'):
                    text += transcription.get('text', '')
            elif event in ['task-finished', 'task-failed']:
                break
        return text

    async def run_asr_tasks(self, pcm_data, model_name):
        task_id = uuid.uuid4().hex
        headers = {'Authorization': f"Bearer {os.getenv('API_KEY')}"}
        async with websockets.connect(os.getenv('WSS_URL'), additional_headers=headers) as ws:
            await ws.send(json.dumps({
                'header': {
                    'streaming': 'duplex',
                    'task_id': task_id,
                    'action': 'run-task',
                },
                'payload': {
                    'model': model_name,
                    'parameters': {
                        'sample_rate': 16000,
                        'format': 'pcm',
                        'transcription_enabled': True,
                    },
                    'input': {},
                    'task': 'asr',
                    'task_group': 'audio',
                    'function': 'recognition',
                },
            }))
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break
            _, text = await asyncio.gather(
                self.asr_sender(pcm_data, ws, task_id),
                self.asr_receiver(ws),
            )
            return text
