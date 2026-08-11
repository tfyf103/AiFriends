# AiFriends English Learning Hub

🌐 **Language:** [简体中文](./README.md) | **English**

> This page is the English navigation hub for learning AiFriends. It is designed for developers who want to understand not only how to run the project, but how the full-stack AI system is engineered, tested, debugged, and maintained.

AiFriends has two learning stages:

```text
Chapter 00–13
Build a complete full-stack AI application from the ground up

Chapter 14–20
Turn an AI demo into a more reliable engineering project
```

The English documentation currently focuses on the highest-value onboarding and architecture material, plus six core labs that explain the most distinctive parts of the project.

---

# 1. Choose your path

## A. I am new to full-stack AI

Use this order:

```text
README_EN
  ↓
QUICK_START_EN
  ↓
AI_MODE=mock
  ↓
Chapter 00
  ↓
Chapter 06 → 07 → 08 → 10
  ↓
Chapter 13 Capstone
  ↓
ARCHITECTURE_EN
```

Recommended links:

- [English Quick Start](./QUICK_START_EN.md)
- [English Architecture Guide](./ARCHITECTURE_EN.md)
- [English Labs](../labs/en/README.md)

## B. I already know Vue or Django and want AI engineering

Focus on:

```text
Chapter 06  Basic LLM Chat
   ↓
Chapter 07  SSE Streaming
   ↓
Chapter 08  LangGraph + Tools
   ↓
Chapter 10  RAG + LanceDB
   ↓
Chapter 13  Full-system Capstone
```

These chapters explain the transition from a normal web application into an agentic, retrieval-augmented, streaming AI system.

## C. I already know LangChain and want the system design

Start here:

```text
ARCHITECTURE_EN
   ↓
backend/web/views/friend/message/chat/chat.py
   ↓
backend/web/views/friend/message/chat/graph.py
   ↓
backend/web/views/friend/message/memory/
   ↓
backend/web/documents/
   ↓
frontend/src/components/character/chat_field/input_field/InputField.vue
   ↓
frontend/src/js/http/streamApi.js
```

---

# 2. English documentation available now

| Resource | Purpose |
|---|---|
| [README_EN](../README_EN.md) | Project overview, features, maintenance, CI, security, contribution |
| [QUICK_START_EN](./QUICK_START_EN.md) | Zero-API-key first run with `AI_MODE=mock` |
| [ARCHITECTURE_EN](./ARCHITECTURE_EN.md) | End-to-end architecture and data flow |
| [English Labs](../labs/en/README.md) | Hands-on labs for the highest-value chapters |
| [SECURITY](../SECURITY.md) | Vulnerability reporting and security scope |
| [CONTRIBUTING](../CONTRIBUTING.md) | Contribution workflow and checks |

The deeper course is still being translated incrementally. The Chinese versions remain the canonical source for chapters that do not yet have an English translation.

---

# 3. English labs available now

| Chapter | Lab | What you build |
|---|---|---|
| 00 | [Environment & Reproducible Setup](../labs/en/chapter-00-environment.md) | Python/Node/Git environment, Django and Vite running |
| 06 | [Minimal LLM Chat](../labs/en/chapter-06-basic-chat.md) | Browser → Django → LLM → JSON response |
| 07 | [SSE Streaming Chat](../labs/en/chapter-07-sse.md) | Streaming tokens, optimistic UI, message persistence |
| 08 | [LangGraph Tool Calling](../labs/en/chapter-08-langgraph-tools.md) | SystemPrompt, context, Agent loop, ToolNode |
| 10 | [RAG + LanceDB](../labs/en/chapter-10-rag.md) | Chunking, embeddings, retrieval, RAG Tool |
| 13 | [Full-System Capstone](../labs/en/chapter-13-capstone.md) | Trace and modify one message across the entire stack |

Why these six first?

```text
00 = reproducibility
06 = minimal LLM boundary
07 = streaming protocol
08 = agent execution model
10 = retrieval-augmented generation
13 = full-stack systems thinking
```

Together they form a compact English learning path through the core ideas that make AiFriends different from a simple LLM API demo.

---

# 4. Runtime modes

AiFriends supports three runtime modes.

## `mock`

Best for the first run and CI.

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

No real model credentials are required, but the request still travels through the real application layers:

```text
Vue
  ↓
JWT
  ↓
Django
  ↓
Friend
  ↓
SSE
  ↓
Message persistence
```

## `text`

Use a real chat model while keeping RAG and speech optional.

## `full`

Enable the full Chat + RAG + ASR + TTS pipeline.

Recommended learning progression:

```text
mock
  ↓
text
  ↓
text + RAG
  ↓
text + ASR
  ↓
full
```

---

# 5. Machine feedback

Do not judge correctness only by whether the UI “looks right.”

## Environment

```bash
cd backend
python manage.py doctor
```

## Chapter structural grader

From the repository root:

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

## Frontend checks

```bash
cd frontend
npm run check
```

Pull requests run GitHub Actions for Python compilation, course grading, migration drift, Django checks/tests, frontend tests/build, VAD asset preparation, and the learning Docker image.

---

# 6. How to debug the project

When “chat is broken,” do not jump directly into LangGraph.

Use a layered order:

```text
UI event
  ↓
Vue state
  ↓
Browser Network
  ↓
JWT / refresh
  ↓
Django URL
  ↓
View / Serializer
  ↓
ORM / ownership
  ↓
AI mode / config
  ↓
LLM
  ↓
Tool / RAG
  ↓
SSE
  ↓
ASR / TTS
```

The Capstone lab requires you to gather real evidence from DevTools and Django logs instead of answering from memory.

---

# 7. Translation status

Current English coverage:

- [x] English project landing page
- [x] English learning hub
- [x] English Quick Start
- [x] English Architecture guide
- [x] High-value labs: 00 / 06 / 07 / 08 / 10 / 13
- [x] English contribution path
- [ ] Remaining Chapter 01–05 / 09 / 11–12 labs
- [ ] Engineering Chapter 14–20 translations
- [ ] Full English API / database / troubleshooting references

English documentation contributions are welcome. Please keep translations technically faithful to the current code and preserve the project’s teaching style: predictions, TODOs, deliberate failures, acceptance criteria, debugging evidence, tests, and trade-offs.

See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

Return to the [English project homepage](../README_EN.md).
