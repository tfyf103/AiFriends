from django.core.management.base import BaseCommand

from web.models.character import Voice
from web.models.friend import SystemPrompt


class Command(BaseCommand):
    help = 'Create safe local demo Voice/SystemPrompt records for first-time learners.'

    def handle(self, *args, **options):
        voice, voice_created = Voice.objects.get_or_create(
            voice_id='demo-voice',
            defaults={'name': 'Demo Voice（text/mock 模式可占位）'},
        )

        reply_prompt, reply_created = SystemPrompt.objects.get_or_create(
            title='回复',
            order_number=1,
            defaults={
                'prompt': '始终遵守角色设定，回答自然、清楚；不知道的信息不要编造。\n',
            },
        )

        memory_prompt, memory_created = SystemPrompt.objects.get_or_create(
            title='记忆',
            order_number=1,
            defaults={
                'prompt': (
                    '根据原始记忆和最近对话更新长期记忆。只保留对未来交流有帮助的稳定事实；'
                    '不要虚构；冲突时优先采用用户最近明确表达的内容。\n'
                ),
            },
        )

        self.stdout.write(self.style.SUCCESS('AiFriends demo seed complete'))
        self.stdout.write(f"Voice: {'created' if voice_created else 'exists'} - {voice.name}")
        self.stdout.write(f"回复 Prompt: {'created' if reply_created else 'exists'}")
        self.stdout.write(f"记忆 Prompt: {'created' if memory_created else 'exists'}")
        self.stdout.write(
            self.style.WARNING(
                'Demo Voice 只是占位。开启真实 TTS 前，请在 Admin 替换成供应商支持的 voice_id。'
            )
        )
