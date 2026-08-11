#!/usr/bin/env python3
"""Lightweight structural grader for AiFriends Chapter 00–20.

It intentionally uses only the Python standard library so a learner can run it before
installing the full AI stack. Structural checks do not replace behavior tests; they
answer the faster question: "Did I wire the expected concept into the expected layer?"
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = {
    0: [('frontend/package.json', 'vite'), ('backend/manage.py', 'django')],
    1: [('frontend/src/router/index.js', 'createRouter'), ('frontend/src/main.js', 'createApp')],
    2: [('backend/web/models/user.py', 'models.Model'), ('backend/web/models/friend.py', 'class Friend')],
    3: [('frontend/src/js/http/api.js', 'Authorization'), ('backend/web/views/user/account/login.py', 'authenticate')],
    4: [('backend/web/create/character/create.py', 'Character.objects.create'), ('backend/web/models/character.py', 'ImageField')],
    5: [('backend/web/views/friend/get_or_create.py', 'Friend.objects.get_or_create'), ('backend/web/models/friend.py', 'character')],
    6: [('backend/web/views/friend/message/chat/chat.py', 'HumanMessage'), ('backend/web/views/friend/message/chat/graph.py', 'ChatOpenAI')],
    7: [('backend/web/views/friend/message/chat/chat.py', 'StreamingHttpResponse'), ('frontend/src/js/http/streamApi.js', 'fetchEventSource')],
    8: [('backend/web/views/friend/message/chat/graph.py', 'ToolNode'), ('backend/web/views/friend/message/chat/graph.py', 'add_conditional_edges')],
    9: [('backend/web/views/friend/message/memory/update.py', 'friend.memory'), ('backend/web/models/friend.py', 'memory =')],
    10: [('backend/web/documents/utils/custom_embeddings.py', 'embed_query'), ('backend/web/documents/retrieval.py', 'similarity_search')],
    11: [('frontend/src/components/character/chat_field/input_field/Microphone.vue', 'MicVAD'), ('backend/web/views/friend/message/asr/asr.py', 'websockets.connect')],
    12: [('frontend/src/components/character/chat_field/input_field/InputField.vue', 'MediaSource'), ('backend/web/views/friend/message/chat/chat.py', 'tts_sender')],
    13: [('frontend/src/components/character/chat_field/input_field/InputField.vue', 'AbortController'), ('backend/web/views/friend/message/chat/chat.py', 'save_message')],
    14: [('backend/web/tests.py', 'MockChatTests'), ('frontend/tests/singleFlight.test.js', 'node:test')],
    15: [('backend/web/serializers/account.py', 'RegisterSerializer'), ('backend/web/views/user/account/register.py', 'status=409')],
    16: [('backend/web/ai/config.py', 'AI_MODE'), ('.env.example', 'AI_MODE=mock')],
    17: [('frontend/src/js/http/streamApi.js', 'signal: options.signal'), ('backend/web/views/friend/message/chat/chat.py', 'cancel_event')],
    18: [('backend/web/models/friend.py', 'UniqueConstraint'), ('backend/web/migrations/0008_friend_unique_constraint.py', 'merge_duplicate_friends')],
    19: [('backend/web/documents/retrieval.py', 'document_source'), ('scripts/eval_rag.py', 'Retrieval eval')],
    20: [('.github/workflows/ci.yml', 'docker-learning-image'), ('backend/web/views/health.py', 'HealthView'), ('Dockerfile.learning', 'frontend-builder')],
}


def run(chapter: int) -> int:
    checks = []
    for number in range(chapter + 1):
        checks.extend((number, *check) for check in CHECKS.get(number, []))

    failures = 0
    for number, relative, marker in checks:
        path = ROOT / relative
        if not path.exists():
            print(f'[✗] Chapter {number:02d}: missing {relative}')
            failures += 1
            continue
        text = path.read_text(encoding='utf8', errors='ignore')
        if marker not in text:
            print(f'[✗] Chapter {number:02d}: {relative} missing marker {marker!r}')
            failures += 1
        else:
            print(f'[✓] Chapter {number:02d}: {relative} → {marker}')

    if failures:
        print(f'\n{failures} structural check(s) failed.')
        return 1
    print(f'\nChapter 00–{chapter:02d} structural checks passed.')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--chapter', type=int, default=20, choices=range(21))
    args = parser.parse_args()
    raise SystemExit(run(args.chapter))
