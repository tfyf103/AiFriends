# AiFriends English Learning Hub

🌐 **Language:** [简体中文](./README.md) | **English**

> This is the English navigation hub for learning AiFriends. The English track now covers the **complete Chapter 00–20 lab curriculum**, real Git-history engineering archaeology, core architecture/API/database references, bilingual terminology, real screenshots/GIFs, and a Browser E2E example.

AiFriends has two learning stages:

```text
Chapter 00–13
Build a complete full-stack AI application from the ground up

Chapter 14–20
Turn an AI demo into a more reliable engineering project
```

The code, tests, grader, CI, security policy, terminology baseline, and contribution workflow are shared by Chinese and English learners.

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
Chapter 00 → 01 → 02 → 03 → 04 → 05
  ↓
Chapter 06 → 07 → 08 → 09 → 10 → 11 → 12
  ↓
Chapter 13 Capstone
  ↓
Chapter 14 → 15 → 16 → 17 → 18 → 19 → 20
  ↓
ARCHITECTURE_EN / API / ER / Troubleshooting
```

Recommended entry points:

- [English Quick Start](./QUICK_START_EN.md)
- [English Labs 00–20](../labs/en/README.md)
- [English Architecture Guide](./ARCHITECTURE_EN.md)

## B. I know Vue/Django and want the AI application path

Focus on:

```text
06 Basic LLM Chat
  ↓
07 SSE Streaming
  ↓
08 LangGraph Tool Calling
  ↓
09 Long-Term Memory
  ↓
10 RAG + LanceDB
  ↓
11 ASR
  ↓
12 Streaming TTS
  ↓
13 Full-System Capstone
```

## C. I already know AI frameworks and want engineering/maintenance

Use:

```text
14 Testing / TDD
  ↓
15 DRF Engineering
  ↓
16 Config / Providers
  ↓
17 Streaming / Cancellation
  ↓
18 Data / Security
  ↓
19 RAG / Memory Evaluation
  ↓
20 CI / Deploy / Observability
```

Start with [English Engineering Course](./ENGINEERING_COURSE_EN.md).

## D. I want to understand the maintained system quickly

Read:

```text
ARCHITECTURE_EN
  ↓
API_REFERENCE_EN
  ↓
DATABASE_ER_EN
  ↓
TROUBLESHOOTING_EN
  ↓
source code + tests + CI
```

## E. I want to understand how AiFriends actually evolved

Use the real Git history:

```text
COURSE_REBUILD_EN
  ↓
git show --stat <historical-sha>
  ↓
git show <historical-sha>
  ↓
compare historical design with current main
```

Start with [Rebuild AiFriends from Scratch — Real Git History](./COURSE_REBUILD_EN.md).

---

# 2. Complete English documentation

| Resource | Purpose |
|---|---|
| [README_EN](../README_EN.md) | Project overview, live demo, maintenance, security, contribution |
| [QUICK_START_EN](./QUICK_START_EN.md) | Zero-API-key first run with `AI_MODE=mock` |
| [COURSE_REBUILD_EN](./COURSE_REBUILD_EN.md) | Real Git-history engineering archaeology and rebuild path |
| [ARCHITECTURE_EN](./ARCHITECTURE_EN.md) | End-to-end architecture and request/data flow |
| [English Labs 00–20](../labs/en/README.md) | Complete hands-on curriculum |
| [ENGINEERING_COURSE_EN](./ENGINEERING_COURSE_EN.md) | Engineering Chapters 14–20 overview |
| [API_REFERENCE_EN](./API_REFERENCE_EN.md) | Current HTTP/SSE/JWT/API behavior |
| [DATABASE_ER_EN](./DATABASE_ER_EN.md) | Models, relations, constraints, storage boundaries |
| [TROUBLESHOOTING_EN](./TROUBLESHOOTING_EN.md) | Layered debugging guide |
| [BILINGUAL_GLOSSARY](./BILINGUAL_GLOSSARY.md) | Canonical Chinese/English engineering terminology |
| [SCREENSHOTS](./SCREENSHOTS.md) | Real screenshot/GIF gallery and contribution rules |
| [LIVE_DEMO](./LIVE_DEMO.md) | Real production screenshot verification |
| [PRODUCT_EXPERIENCE](./PRODUCT_EXPERIENCE.md) | Evidence-based real-user journey from Character discovery to Friend, Chat, Memory/RAG/Voice |
| [Browser E2E](../e2e/README.md) | English-first Chromium E2E example in Mock mode |
| [GRADING](./GRADING.md) | doctor / grader / tests / CI model |
| [SECURITY](../SECURITY.md) | Vulnerability reporting and security scope |
| [CONTRIBUTING](../CONTRIBUTING.md) | Contribution workflow and checks |

Historical archaeology is now available in English. A few auxiliary notes can still be Chinese-first, but the maintained learning, engineering, visual, testing, and Git-history paths no longer require Chinese prose.

---

# 3. Complete English Labs — Stage 1

| Chapter | Lab | Main question |
|---|---|---|
| 00 | [Environment](../labs/en/chapter-00-environment.md) | Can I reproduce the environment? |
| 01 | [Vue / Router](../labs/en/chapter-01-vue-router.md) | How does the SPA render and navigate? |
| 02 | [Django / ORM](../labs/en/chapter-02-django-orm.md) | How does URL → View → Model → DB work? |
| 03 | [JWT / Pinia / Axios](../labs/en/chapter-03-jwt-auth.md) | How does identity persist across frontend/backend? |
| 04 | [Character CRUD](../labs/en/chapter-04-character-crud.md) | How do CRUD, uploads, Voice, ownership work? |
| 05 | [Homepage / Friend](../labs/en/chapter-05-friend-system.md) | How are Characters discovered and relationships persisted? |
| 06 | [Basic LLM Chat](../labs/en/chapter-06-basic-chat.md) | How does one browser message reach a model? |
| 07 | [SSE](../labs/en/chapter-07-sse.md) | Why can text stream incrementally? |
| 08 | [LangGraph Tools](../labs/en/chapter-08-langgraph-tools.md) | How does an Agent decide and execute Tools? |
| 09 | [Long-Term Memory](../labs/en/chapter-09-memory.md) | How do we compress growing chat history? |
| 10 | [RAG + LanceDB](../labs/en/chapter-10-rag.md) | How does private knowledge enter answers? |
| 11 | [ASR](../labs/en/chapter-11-asr.md) | How does microphone audio become chat text? |
| 12 | [Streaming TTS](../labs/en/chapter-12-tts.md) | How does the Character speak while text streams? |
| 13 | [Capstone](../labs/en/chapter-13-capstone.md) | Can I trace and change one message across all layers? |

---

# 4. Complete English Labs — Stage 2

| Chapter | Lab | Engineering question |
|---|---|---|
| 14 | [Testing / TDD](../labs/en/chapter-14-testing-tdd.md) | What automated evidence protects behavior? |
| 15 | [DRF Engineering](../labs/en/chapter-15-drf-engineering.md) | How should APIs validate and express errors? |
| 16 | [Config / Providers](../labs/en/chapter-16-config-providers.md) | How do runtime modes/providers stay decoupled? |
| 17 | [Cancellation](../labs/en/chapter-17-stream-cancellation.md) | What actually stops when the user clicks Stop? |
| 18 | [Data / Security](../labs/en/chapter-18-data-security.md) | How do constraints, ownership, files, privacy interact? |
| 19 | [RAG / Memory Eval](../labs/en/chapter-19-rag-memory-eval.md) | How do we measure quality and provenance? |
| 20 | [CI / Deploy / Observability](../labs/en/chapter-20-ci-deploy-observability.md) | How do we move beyond “works on my machine”? |

---

# 5. Runtime modes

AiFriends supports:

## `mock`

Best for first run, Browser E2E, and CI:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

No external AI credentials are required, but the request still crosses real layers:

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

Enable the complete Chat + RAG + ASR + TTS path, subject to feature flags and provider configuration.

Recommended progression:

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

# 6. Machine feedback

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

## Bilingual/source drift

```bash
python scripts/check_i18n.py
```

This detects structural drift such as missing paired documents/Labs, moved source sentinels, missing visual assets, and broken important relative links. It does **not** claim to judge semantic translation quality.

## Live-demo GIF drift

```bash
python scripts/build_demo_gif.py --check
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

## Browser E2E

```bash
npm install --prefix e2e
npm exec --prefix e2e -- playwright install chromium
node e2e/browser-smoke.mjs
```

## Repository CI

Pull requests run:

```text
Python compile
internationalization/documentation drift check
live-demo GIF drift check
Chapter 00–20 grader
migration drift check
Django check/tests
npm ci
VAD setup
frontend quality/tests/build
Chromium Browser E2E in AI_MODE=mock
learning Docker image build
```

---

# 7. Layered debugging order

When “chat is broken,” do not jump directly into LangGraph.

```text
UI event
  ↓
Vue state
  ↓
Browser Network
  ↓
JWT / refresh
  ↓
Django URL / View / Serializer
  ↓
ORM / ownership / constraints
  ↓
AI mode / feature config
  ↓
LLM
  ↓
Tool / RAG
  ↓
SSE / cancellation
  ↓
ASR / TTS / browser audio
```

Use [English Troubleshooting](./TROUBLESHOOTING_EN.md) for detailed failure cases.

---

# 8. Internationalization quality status

The major internationalization milestones are now implemented:

- [x] English project landing page
- [x] English Learning Hub
- [x] English Quick Start
- [x] English Architecture Guide
- [x] Complete Chapters 00–20 English Labs
- [x] English Engineering Course overview
- [x] English API Reference
- [x] English Database / ER Guide
- [x] English Troubleshooting Guide
- [x] English Git-history `COURSE_REBUILD` archaeology
- [x] Bilingual engineering terminology baseline
- [x] Real bilingual screenshots + reproducible walkthrough GIF
- [x] Structural bilingual/source drift check in CI
- [x] English-first Browser E2E example in Mock mode
- [x] English contribution path

Internationalization is now an ongoing maintenance discipline rather than a one-time translation project. Useful future work includes keeping terminology aligned as features evolve, adding focused real-runtime visuals to high-value Labs, improving accessibility language, and extending E2E coverage when new user-visible flows become stable.

English documentation contributions remain welcome through [CONTRIBUTING.md](../CONTRIBUTING.md).

---

Return to the [English project homepage](../README_EN.md).
