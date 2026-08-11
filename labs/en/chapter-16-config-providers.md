# Chapter 16 Lab: Configuration, Feature Flags, and Model Providers

🌐 **Language:** [中文](../chapter-16-config-providers.md) | **English**

## Goal

Upgrade from:

> “Edit source code every time you switch models or capabilities.”

into:

> **“Runtime configuration decides which capabilities are active.”**

Current AiFriends centralizes AI configuration in:

```text
backend/web/ai/config.py
.env.example
```

Important settings include:

```text
AI_MODE=mock | text | full
ENABLE_RAG
ENABLE_ASR
ENABLE_TTS
CHAT_MODEL
MEMORY_MODEL
EMBEDDING_MODEL
EMBEDDING_DIMENSIONS
ASR_MODEL
TTS_MODEL
API_KEY
API_BASE
WSS_URL
```

---

## TODO 1: Experience all three modes

### Mock

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

You should be able to use:

```text
registration/login
Character/Friend
SSE chat
Message persistence
CI/tests
```

without a real AI API key.

### Text

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

Use a real chat model while keeping speech optional.

### Full

Enable capabilities deliberately:

```env
ENABLE_RAG=true
ENABLE_ASR=true
ENABLE_TTS=true
```

Do not turn everything on at once when debugging. Enable one capability, run diagnostics, then add the next.

---

## TODO 2: Use `doctor` as a configuration contract

```bash
cd backend
python manage.py doctor
```

Deliberately remove one required setting for your selected mode/feature set.

Observe the difference between:

```text
required failure
optional warning
```

### Explain why

A text-only learner should not fail because a speech provider is missing.

A full TTS run **should** fail diagnostics if required TTS configuration is unavailable.

Good diagnostics are mode-aware.

---

## TODO 3: Find hard-coded model names

Search for provider/model identifiers in source.

The target architecture is:

```text
business code
  ↓
get_ai_settings()
  ↓
runtime model/config values
```

rather than:

```text
five separate business files each hard-code one model name
```

### Acceptance

Changing a configured chat model should not require editing unrelated Views, memory code, or RAG orchestration.

---

## TODO 4: Understand feature flags vs permissions

These are different questions:

```text
Feature flag: Is ASR enabled for this deployment?
Permission:   Is this authenticated user allowed to access this resource/action?
```

`ENABLE_RAG=false` is not an authorization system.

Likewise, a user being authenticated does not mean an optional provider capability is configured.

---

## TODO 5: Test feature isolation

Write/inspect automated checks for invariants such as:

```text
mock does not create/call real ChatOpenAI
text does not require WSS by default
ENABLE_RAG=false means RAG tool is not registered
ENABLE_ASR=false returns a clear 503
ENABLE_TTS=false still allows real text chat
Character without Voice can still use text-only chat
```

This is architecture expressed as executable tests.

---

## TODO 6: Design a provider adapter

The current project uses OpenAI-compatible HTTP interfaces for some model calls and provider-specific WebSocket flows for speech.

Design abstractions such as:

```python
class ChatProvider:
    def create_model(self): ...

class EmbeddingProvider:
    def embed_documents(self, texts): ...

class ASRProvider:
    async def transcribe(self, pcm): ...

class TTSProvider:
    async def stream_audio(self, text_stream, voice): ...
```

### What can OpenAI compatibility unify?

Potentially:

```text
request/response shape
chat model client
some streaming conventions
some tool-calling schema
```

### What often remains provider-specific?

```text
model names
available dimensions
usage metadata
rate limits
Tool Calling quirks
ASR/TTS WebSocket payloads
audio formats
voice identifiers
error codes
```

Do not hide real incompatibilities behind a fake universal interface.

---

## TODO 7: Keep secrets out of configuration files committed to Git

`.env.example` should document names and safe defaults/placeholders.

Real values such as:

```text
API_KEY
Django SECRET_KEY
provider credentials
JWTs
```

must not be committed.

### Acceptance

Run:

```bash
git status
```

and confirm your real `.env` is ignored.

---

## TODO 8: Think about provider fallback

Design—not necessarily implement—policy for:

```text
primary chat provider unavailable
RAG embedding provider unavailable
TTS unavailable but text model healthy
ASR unavailable but keyboard input healthy
```

For each case decide:

```text
fail whole request?
degrade one feature?
retry?
fall back to another provider?
show explicit UI state?
```

The current text-only fallback around optional speech is one example of graceful degradation.

---

## Acceptance

- [ ] You can explain `mock`, `text`, and `full`.
- [ ] You can use `doctor` to find missing required configuration.
- [ ] Switching models is centralized instead of scattered through business code.
- [ ] You can distinguish a feature flag from user authorization.
- [ ] You can explain why `.env.example` must not contain real secrets.
- [ ] You can identify what an OpenAI-compatible API does **not** standardize.

---

## Challenge

Add a fourth provider path, for example a local model or another OpenAI-compatible service, with this design goal:

```text
business Views unchanged
LangGraph topology unchanged
provider/config layer extended
```

Then document:

- how provider selection is configured;
- what capabilities are actually compatible;
- what tests prove the adapter does not break Mock mode;
- how errors/degradation are surfaced.
