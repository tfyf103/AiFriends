# AiFriends Browser E2E / 浏览器端到端示例

**English-first example with Chinese notes / 英文优先示例，附中文说明**

This directory contains a real-browser smoke test for the maintained AiFriends stack. It is intentionally small: the goal is to teach what Browser E2E means without turning the course into a large Playwright framework.

本目录提供一个真实浏览器 Smoke Test，目的是让学习者理解 Browser E2E 如何跨越前端、HTTP、后端和数据库，而不是额外引入一套庞大测试框架。

---

## What it proves / 它验证什么

`browser-smoke.mjs` starts a temporary learning environment and checks:

```text
Chromium
  ↓
Vite / Vue
  ↓
/api proxy
  ↓
Django / DRF
  ↓
SQLite temp database
```

The current smoke flow verifies:

1. the browser title is `AiFriends` rather than the Vite scaffold default;
2. a user can register through the real browser form and backend API;
3. the authenticated browser can enter the protected `/friend` route;
4. authentication is restored after a browser reload;
5. the whole run uses `AI_MODE=mock`, so no external LLM/RAG/ASR/TTS credentials are needed.

当前测试会验证浏览器标题、真实注册链路、受保护 Friend 页面访问、刷新后的登录恢复，并强制使用 Mock 模式。

---

## Why this is E2E / 为什么它属于 E2E

A unit test may call one function. This test crosses real process and protocol boundaries:

```text
DOM input
  ↓
Vue event handling
  ↓
Axios
  ↓
Vite proxy
  ↓
Django URL / View
  ↓
Serializer / auth
  ↓
SQLite
  ↓
HTTP response
  ↓
Pinia / Router
  ↓
DOM + protected navigation
```

That is why it complements — rather than replaces — Node unit tests and Django behavior tests.

---

## Run locally / 本地运行

Prerequisites:

- Python environment with `requirements.txt` installed;
- frontend dependencies installed with `npm ci`;
- Node 22+ recommended;
- Playwright Chromium installed.

Install the E2E package:

```bash
npm install --prefix e2e
npm exec --prefix e2e playwright install chromium
```

Run:

```bash
node e2e/browser-smoke.mjs
```

The script itself:

- creates `e2e/.tmp/e2e.sqlite3`;
- runs migrations;
- starts Django on `127.0.0.1:8000`;
- starts Vite on `127.0.0.1:5173`;
- launches Chromium;
- creates only temporary local E2E data;
- writes a diagnostic screenshot to `e2e/artifacts/`;
- stops both servers when finished.

It does **not** use the public production database.

---

## CI / 持续集成

The repository CI installs Playwright in a dedicated `browser-e2e` job and runs this script after the ordinary backend/frontend checks.

The job is intentionally independent from real AI providers:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

This keeps contributions reproducible and prevents API keys from becoming a test prerequisite.

---

## Extend the test carefully / 如何扩展

High-value future E2E cases include:

- SSE text visibly appends instead of arriving only at the end;
- browser cancellation stops an active Mock stream;
- duplicate registration displays the expected error contract;
- Character creation/update with safe fixture images;
- Friend uniqueness behavior;
- RAG citation UI once first-class citation events exist;
- accessibility keyboard paths for login/register/chat.

Do not make the E2E job depend on external model providers unless the test is explicitly separated from the default contributor CI.

Related:

- [English Chapter 14 — Testing/TDD](../labs/en/chapter-14-testing-tdd.md)
- [English Chapter 17 — Streaming/Cancellation](../labs/en/chapter-17-streaming-cancellation.md)
- [Bilingual terminology guide](../docs/BILINGUAL_GLOSSARY.md)
- [Screenshot & GIF guide](../docs/SCREENSHOTS.md)
