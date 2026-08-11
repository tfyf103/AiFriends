import os
import sys
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection

from web.ai.config import get_ai_settings
from web.models.character import Voice
from web.models.friend import SystemPrompt


class Command(BaseCommand):
    help = 'Check whether the local AiFriends learning environment is ready.'

    def handle(self, *args, **options):
        config = get_ai_settings()
        failures = 0

        def ok(message):
            self.stdout.write(self.style.SUCCESS(f'[✓] {message}'))

        def warn(message):
            self.stdout.write(self.style.WARNING(f'[!] {message}'))

        def fail(message):
            nonlocal failures
            failures += 1
            self.stdout.write(self.style.ERROR(f'[✗] {message}'))

        self.stdout.write(self.style.MIGRATE_HEADING('AiFriends doctor'))
        self.stdout.write(f'AI mode: {config.mode}\n')

        if sys.version_info >= (3, 12):
            ok(f'Python {sys.version.split()[0]}')
        else:
            fail(f'Python {sys.version.split()[0]}；项目建议 3.12+')

        try:
            connection.ensure_connection()
            ok('Database connection')
        except Exception as exc:
            fail(f'Database connection: {exc}')

        if config.is_mock:
            ok('Mock mode: API_KEY / API_BASE / WSS_URL are not required')
        else:
            for name in ['API_KEY', 'API_BASE']:
                if os.getenv(name):
                    ok(name)
                else:
                    fail(f'{name} missing')

        if config.enable_asr or config.enable_tts:
            if os.getenv('WSS_URL'):
                ok('WSS_URL')
            else:
                fail('WSS_URL missing while speech is enabled')

        if SystemPrompt.objects.filter(title='回复').exists():
            ok("SystemPrompt title='回复'")
        else:
            warn("SystemPrompt title='回复' missing; run python manage.py seed_demo")

        if SystemPrompt.objects.filter(title='记忆').exists():
            ok("SystemPrompt title='记忆'")
        else:
            warn("SystemPrompt title='记忆' missing; run python manage.py seed_demo")

        if Voice.objects.exists():
            ok('Voice data exists')
        elif config.enable_tts:
            fail('No Voice rows while TTS is enabled')
        else:
            warn('No Voice rows; fine for mock/text-only learning')

        if config.enable_rag:
            rag_path = Path(settings.BASE_DIR) / 'web' / 'documents' / 'lancedb_storage'
            if rag_path.exists():
                ok('LanceDB storage exists')
            else:
                fail('RAG enabled but LanceDB storage is missing')

        if config.enable_asr:
            vad_path = Path(settings.BASE_DIR).parent / 'frontend' / 'public' / 'vad'
            if vad_path.exists() and any(vad_path.iterdir()):
                ok('VAD browser assets exist')
            else:
                fail('VAD assets missing; run cd frontend && npm run setup:vad')

        if failures:
            raise SystemExit(1)

        self.stdout.write(self.style.SUCCESS('\nEnvironment is ready for the selected AI mode.'))
