from pathlib import Path


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f'missing documentation anchor: {label}')
    return text.replace(old, new, 1)


def main() -> None:
    zh_api_path = Path('docs/API_REFERENCE.md')
    en_api_path = Path('docs/API_REFERENCE_EN.md')
    zh_er_path = Path('docs/DATABASE_ER.md')
    en_er_path = Path('docs/DATABASE_ER_EN.md')

    zh = zh_api_path.read_text(encoding='utf-8')
    en = en_api_path.read_text(encoding='utf-8')
    zh_er = zh_er_path.read_text(encoding='utf-8')
    en_er = en_er_path.read_text(encoding='utf-8')

    zh = replace_required(
        zh,
        '| POST | `/api/user/account/logout/` | Bearer | empty | JSON | 删除 refresh cookie |',
        '| POST | `/api/user/account/logout/` | Bearer | empty | JSON | 撤销 refresh token + 删除 Cookie |',
        'zh logout table',
    )
    zh = replace_required(
        zh,
        '404 Not Found\n409 Conflict\n503 Service Unavailable',
        '404 Not Found\n409 Conflict\n413 Payload Too Large\n502 Bad Gateway\n503 Service Unavailable',
        'zh status list',
    )
    zh = replace_required(
        zh,
        '并轮换 refresh cookie。\n\n缺少 / 过期：',
        '并轮换 refresh cookie。当前启用了 SimpleJWT token blacklist：**本次已经使用过的旧 refresh token 会立即进入 blacklist，不能再次重放换取 access。**\n\n缺少 / 过期 / 已撤销：',
        'zh refresh rotation',
    )
    zh = replace_required(
        zh,
        '后端删除 refresh cookie，前端同时清 Pinia。',
        '后端会先将当前 refresh token 加入 blacklist，再删除 refresh cookie；前端同时清 Pinia。仅删除 Cookie 不等于撤销凭证，所以服务端 blacklist 是 logout 安全语义的一部分。',
        'zh logout details',
    )
    zh = replace_required(
        zh,
        '这个 API 仍然是 Chapter 15 很好的 Serializer 重构对象。',
        '上传头像会在写入前校验真实图片内容，只接受 JPEG / PNG / WebP，单张最多 8 MB、最多 2500 万像素；数据库中的用户名与 UserProfile 元数据使用事务保持一致。\n\n这个 API 仍然是 Chapter 15 很好的 Serializer 重构对象。',
        'zh profile upload',
    )
    zh = replace_required(
        zh,
        'Character.objects.create\n ↓\nSQLite + media',
        '图片格式 / 大小 / 像素校验\n ↓\nCharacter.objects.create\n ↓\nSQLite + media',
        'zh create flow',
    )
    zh = replace_required(
        zh,
        'Chapter 17 Challenge：设计：',
        '正常完成路径会先 `Message.objects.create(...)`，然后才发送 SSE `[DONE]`，避免客户端收到完成标记立即断开时丢失最后一条消息。\n\nChapter 17 Challenge：设计：',
        'zh persistence order',
    )
    zh = replace_required(
        zh,
        '每次最多 10 条 Message 记录。\n\n后端额外限制：',
        '每次最多 10 条 Message 记录。`last_message_id` 非整数/负数返回 HTTP 400；Friend 不存在或不属于当前用户返回 HTTP 404。\n\n后端额外限制：',
        'zh history validation',
    )
    zh = replace_required(
        zh,
        '这样文本学习不会因为没有 Speech Account 莫名失败。',
        '这样文本学习不会因为没有 Speech Account 莫名失败。启用 ASR 后，PCM 上传在读取前限制为最多 **5 MB**；超过限制返回 HTTP 413，第三方 ASR Provider 调用失败返回 HTTP 502。',
        'zh asr limits',
    )

    en = replace_required(
        en,
        'The refresh cookie is rotated according to the current JWT/cookie configuration.\n\nMissing/invalid/expired refresh credentials result in an authentication failure rather than a successful empty response.',
        'The refresh cookie is rotated according to the current JWT/cookie configuration. SimpleJWT token blacklisting is enabled: **the refresh credential used for a successful rotation is immediately revoked and cannot be replayed to mint another access token.**\n\nMissing, invalid, expired, or revoked refresh credentials result in an authentication failure rather than a successful empty response.',
        'en refresh rotation',
    )
    en = replace_required(
        en,
        'The backend removes the refresh cookie and the frontend clears its user/access state.\n\n> Current project cleanup removes the cookie. Full refresh-token blacklist/revocation integration remains a separate hardening step.',
        'The backend first blacklists the current refresh token, then removes the refresh cookie; the frontend clears its user/access state. Deleting a browser cookie alone is not credential revocation, so server-side blacklisting is part of the logout contract.',
        'en logout details',
    )
    en = replace_required(
        en,
        'This endpoint remains a useful Chapter 15 Serializer/error-contract refactoring target.',
        'Avatar uploads are verified before storage. Only real JPEG / PNG / WebP images are accepted, with an 8 MB byte limit and a 25-million-pixel limit. Username + UserProfile metadata writes are kept in one database transaction.\n\nThis endpoint remains a useful Chapter 15 Serializer/error-contract refactoring target.',
        'en profile upload',
    )
    en = replace_required(
        en,
        'resolve Voice\n  ↓\nCharacter.objects.create(...)',
        'resolve Voice\n  ↓\nvalidate image bytes / dimensions\n  ↓\nCharacter.objects.create(...)',
        'en create flow',
    )
    en = replace_required(
        en,
        'Current code intentionally distinguishes normal completion from cancelled streams.',
        'Current code intentionally distinguishes normal completion from cancelled streams. On normal completion, Message persistence happens **before** the SSE `[DONE]` marker so a client closing immediately after completion cannot race the final database write.',
        'en persistence order',
    )
    en = replace_required(
        en,
        "The backend scopes history by the authenticated user so another user's Friend history cannot be read by changing the ID.",
        "The backend scopes history by the authenticated user so another user's Friend history cannot be read by changing the ID. Invalid/negative cursors return HTTP 400; a missing or inaccessible Friend returns HTTP 404.",
        'en history validation',
    )
    en = replace_required(
        en,
        'This is intentional feature isolation: text learning should not fail because the learner has no speech account.',
        'This is intentional feature isolation: text learning should not fail because the learner has no speech account. When ASR is enabled, PCM uploads are bounded to **5 MB before reading into memory**; oversized audio returns HTTP 413 and upstream speech-provider failures return HTTP 502.',
        'en asr limits',
    )

    zh_er = replace_required(
        zh_er,
        '当前工程化实现中 TTS 是可选能力；关闭 TTS 时，没有有效 Voice 也不应阻断纯文本聊天。',
        '当前工程化实现中 TTS 是可选能力；关闭 TTS 时，没有有效 Voice 也不应阻断纯文本聊天。`Character.voice` 使用 `on_delete=SET_NULL`：删除/下线一个 Voice 只会把相关 Character 的 `voice_id` 置空，**不会级联删除用户创建的 Character、Friend 或 Message 历史**。',
        'zh voice set null',
    )
    en_er = replace_required(
        en_er,
        'TTS is optional. The maintained chat path can run text-only when TTS is disabled, and a missing Voice should not make text chat impossible when speech is not required.',
        'TTS is optional. The maintained chat path can run text-only when TTS is disabled, and a missing Voice should not make text chat impossible when speech is not required. `Character.voice` uses `on_delete=SET_NULL`: retiring/deleting a Voice clears the Character voice reference instead of cascade-deleting user-authored Characters, Friends, or Message history.',
        'en voice set null',
    )

    zh_api_path.write_text(zh, encoding='utf-8')
    en_api_path.write_text(en, encoding='utf-8')
    zh_er_path.write_text(zh_er, encoding='utf-8')
    en_er_path.write_text(en_er, encoding='utf-8')


if __name__ == '__main__':
    main()
