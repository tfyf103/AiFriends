# AiFriends English Labs

🌐 **Language:** [中文 Labs](../README.md) | **English**

> Goal: move from “I understand the explanation” to “I can implement it, break it on purpose, debug it, and prove it works.”

The English track now covers the **complete Chapter 00–20 curriculum**.

```text
Chapter 00–13 → build the full-stack AI application
Chapter 14–20 → make the AI demo testable, safer, maintainable, deployable, and observable
```

The English labs are not summary translations. They preserve the project's teaching format:

```text
prediction
TODO
small working loop
deliberate failure
acceptance criteria
common errors
challenge
machine feedback
engineering trade-offs
```

---

# Recommended learning path

For a full beginner path:

```text
English Project README
      ↓
English Learning Hub
      ↓
English Quick Start
      ↓
AI_MODE=mock
      ↓
Chapter 00 → 01 → 02 → 03 → 04 → 05
      ↓
Chapter 06 → 07 → 08 → 09 → 10 → 11 → 12
      ↓
Chapter 13 Capstone
      ↓
Chapter 14 → 15 → 16 → 17 → 18 → 19 → 20
      ↓
English Architecture / API / ER / Troubleshooting
```

If you already know web development and want the AI-specific core:

```text
06 Basic LLM Chat
  ↓
07 SSE Streaming
  ↓
08 LangGraph Tool Calling
  ↓
09 Long-term Memory
  ↓
10 RAG + LanceDB
  ↓
11 ASR
  ↓
12 Streaming TTS
  ↓
13 Capstone
```

If you mainly want engineering/maintainer practice:

```text
14 Testing / TDD
15 DRF Engineering
16 Config / Providers
17 Cancellation
18 Data / Security
19 RAG / Memory Evaluation
20 CI / Deploy / Observability
```

---

# Stage 1 — Chapters 00–13: Build the System

| Chapter | English Lab | What you build/prove |
|---|---|---|
| 00 | [Environment & Reproducible Setup](./chapter-00-environment.md) | Python/Node/Git, Django + Vite, Mock first run |
| 01 | [Vue Pages, Components & Router](./chapter-01-vue-router.md) | SPA routing, components, reactive state |
| 02 | [Django, ORM, Migrations & SQLite](./chapter-02-django-orm.md) | URL → View → Model → DB mental model |
| 03 | [JWT, Pinia & Axios](./chapter-03-jwt-auth.md) | registration/login, refresh cookie, single-flight refresh |
| 04 | [Character CRUD, Uploads & Voice](./chapter-04-character-crud.md) | CRUD, multipart files, ownership, Voice relation |
| 05 | [Homepage, Search & Friend](./chapter-05-friend-system.md) | discovery, infinite loading, Friend uniqueness |
| 06 | [Minimal LLM Chat](./chapter-06-basic-chat.md) | Browser → Django → LLM minimal loop |
| 07 | [SSE Streaming Chat](./chapter-07-sse.md) | streaming, refresh, persistence, cancellation |
| 08 | [LangGraph Tool Calling](./chapter-08-langgraph-tools.md) | SystemPrompt, context, ToolNode, routing |
| 09 | [Long-Term Memory](./chapter-09-memory.md) | compress recent history into `Friend.memory` |
| 10 | [RAG + LanceDB](./chapter-10-rag.md) | chunking, embeddings, retrieval, eval, sources |
| 11 | [ASR](./chapter-11-asr.md) | microphone/PCM → WebSocket ASR → normalized text |
| 12 | [Streaming TTS](./chapter-12-tts.md) | LLM text + TTS audio streaming and playback |
| 13 | [Full-System Capstone](./chapter-13-capstone.md) | trace, debug, and modify one cross-layer message flow |

---

# Stage 2 — Chapters 14–20: Engineer the System

| Chapter | English Lab | Engineering capability |
|---|---|---|
| 14 | [Testing / TDD](./chapter-14-testing-tdd.md) | regression evidence, red→green, grader vs tests |
| 15 | [DRF Engineering](./chapter-15-drf-engineering.md) | Serializer, validation, HTTP status, error contracts |
| 16 | [Config / Feature Flags / Providers](./chapter-16-config-providers.md) | `mock/text/full`, runtime models, graceful degradation |
| 17 | [Async / Streaming / Cancellation](./chapter-17-stream-cancellation.md) | AbortController, Queue, sentinel, `cancel_event` |
| 18 | [Data / Security](./chapter-18-data-security.md) | constraints, safe migration, uploads, ownership, privacy |
| 19 | [RAG / Memory Evaluation](./chapter-19-rag-memory-eval.md) | eval sets, provenance, citations, structured memory |
| 20 | [CI / Deploy / Observability](./chapter-20-ci-deploy-observability.md) | GitHub Actions, build, health, logs, Docker, metrics |

Engineering overview: [English Engineering Course](../../docs/ENGINEERING_COURSE_EN.md).

---

# How to use the labs

Do not perform every experiment directly on `main`.

Create a learning branch:

```bash
git switch main
git pull
git switch -c learn/aifriends
```

AiFriends also preserves real Git history. Historical commits are useful engineering archaeology, but may contain bugs or incomplete behavior that was fixed later.

Use this model:

```text
historical commit = how the project evolved
current tests      = current reference behavior
lab acceptance     = learning objective
```

After each lab:

```bash
git add .
git commit -m "learn: finish chapter 07 sse streaming"
```

---

# The eight-step lab loop

1. **Predict first** — which files/layers should data cross?
2. Build the **smallest working loop**.
3. Identify acceptance criteria before adding complexity.
4. Keep DevTools and Django logs visible.
5. Change one layer at a time.
6. Create a deliberate failure and diagnose it.
7. Run grader/tests/build instead of trusting visual inspection.
8. Commit and explain the trade-off in your own words.

---

# Machine feedback

## Environment

```bash
cd backend
python manage.py doctor
```

## Structural grader

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Backend behavior tests

```bash
cd backend
python manage.py test web
```

## Frontend quality/tests/build

```bash
cd frontend
npm run check
```

Pull requests run the repository-wide GitHub Actions workflow in a clean environment.

---

# What “finished” means

A finished lab is not only a page that looks approximately right.

You should be able to answer:

- Which Vue file sends the request?
- What URL, method, headers, and body are used?
- Which Django View receives it?
- Which Models/data stores are read or written?
- Which messages/evidence enter the model?
- How does streaming data return?
- How is cancellation propagated?
- Where is ownership enforced?
- Which failure signal would you inspect first?
- Which automated check protects the important behavior?
- What trade-off did the design make?

---

# Complete English documentation

- [English Project README](../../README_EN.md)
- [English Learning Hub](../../docs/README_EN.md)
- [English Quick Start](../../docs/QUICK_START_EN.md)
- [English Architecture Guide](../../docs/ARCHITECTURE_EN.md)
- [English Engineering Course](../../docs/ENGINEERING_COURSE_EN.md)
- [English API Reference](../../docs/API_REFERENCE_EN.md)
- [English Database / ER Guide](../../docs/DATABASE_ER_EN.md)
- [English Troubleshooting](../../docs/TROUBLESHOOTING_EN.md)
- [Security Policy](../../SECURITY.md)
- [Contributing](../../CONTRIBUTING.md)

English documentation improvements are still welcome—especially terminology consistency, examples, screenshots, accessibility, and keeping translations synchronized with code changes.
