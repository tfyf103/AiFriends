from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from web.ai.config import get_ai_settings


class HealthView(APIView):
    """Small public readiness snapshot with no secrets or private data."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        database = 'ok'
        status_code = 200
        try:
            connection.ensure_connection()
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        except Exception:
            database = 'error'
            status_code = 503

        config = get_ai_settings()
        return Response({
            'status': 'ok' if database == 'ok' else 'degraded',
            'database': database,
            'ai_mode': config.mode,
            'features': {
                'rag': config.enable_rag,
                'asr': config.enable_asr,
                'tts': config.enable_tts,
            },
            'request_id': getattr(request, 'request_id', None),
        }, status=status_code)
