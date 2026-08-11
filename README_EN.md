# 🤖 AiFriends

[![AiFriends CI](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml/badge.svg)](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

🌐 **Language / 语言:** [简体中文](./README.md) | **English**

> **Build an AI companion with characters, long-term memory, RAG, agents, and voice — then learn how to test, secure, maintain, and ship it.**
>
> An open-source, project-based full-stack AI curriculum and reference application for learning how modern AI products are actually engineered and maintained.

AiFriends uses **Vue 3 + Django + DRF + JWT + LangChain + LangGraph + LanceDB + SSE + WebSocket** to turn a real AI application into a reproducible, testable, progressively engineered learning path.

This is not a “call one LLM API and print the answer” demo. It connects browser UI, authentication, persistence, streaming protocols, agents, RAG, long-term memory, ASR/TTS, automated tests, data integrity, security boundaries, CI, and build workflows in one repository.

> **Documentation status:** this English README is a complete project and onboarding guide. The deep chapter-by-chapter course and many source-code teaching comments are currently **Chinese-first**. English documentation will expand incrementally while code, tests, CI, security policy, and contribution workflows are shared by all users.

---

## 30-second project snapshot

| Area | Current status |
| --- | --- |
| License | **MIT** |
| Maintenance | **Active development**, primarily maintained by `@tfyf103` |
| Languages | Chinese + English landing pages; deep course content currently Chinese-first |
| First-run barrier | `AI_MODE=mock` runs the core Web/SSE flow with **zero API keys** |
| Curriculum | Chapters **00–20**, from beginner foundations to engineering practices |
| Automated feedback | Django tests + Node tests + structural grader + GitHub Actions |
| AI stack | LangGraph Agent / Tool Calling / Memory / RAG / ASR / TTS |
| Engineering stack | Serializers / cancellation / migration checks / Health / Request-ID / Docker learning image |
| Security | [SECURITY.md](./SECURITY.md) |
| Contributing | [CONTRIBUTING.md](./CONTRIBUTING.md) |

> **Project goal:** help learners go beyond “getting an AI demo to work” and understand why the system is designed this way, how to verify it, how to maintain it, and how to evolve it toward reliable software engineering.

---

# Why AiFriends?

Many AI tutorials stop here:

```text
Prompt
  ↓
Model API
  ↓
Print answer
```

Real AI products usually look more like this:

```text
Frontend
  ↓
Authentication
  ↓
HTTP / SSE / WebSocket
  ↓
Backend / ORM
  ↓
LLM / Agent / Tools
  ↓
RAG / Memory
  ↓
Speech
  ↓
Persistence / Tests / CI / Security
```

AiFriends is designed to bridge that engineering gap with a **code-first, reproducible, experiment-driven learning path with automated feedback**.

The tutorial and the maintained application live in the same repository. Learners inspect the real runtime path, real Git history, real tests, real data migrations, and real CI instead of switching to a separate toy implementation.

The project started from the Chinese AI learning community and is now opening a bilingual entry point for developers worldwide.

---

# 🌱 Recommended learning path

```text
README_EN.md: understand the project
   ↓
AI_MODE=mock: run it with zero API keys
   ↓
Understand one complete request path
   ↓
Explore source + architecture
   ↓
Chapters 00–13: build the AI application
   ↓
Chapters 14–20: testing / security / CI / deployment
   ↓
Contribute fixes, tests, evaluations, or docs
```

## Main resources

The following deep-learning materials are currently Chinese-first, but the code paths and commands are the same:

- 📘 [Learning Center / 学习中心](./docs/README.md)
- 🚀 [Beginner Tutorial / 完整运行与复刻教程](./docs/BEGINNER_TUTORIAL.md)
- 🧭 [Rebuild from Git History / 沿真实 Git 历史重建](./docs/COURSE_REBUILD.md)
- 🧪 [Labs: Chapter 00–20](./labs/README.md)
- 🏗️ [Engineering Course: Chapter 14–20](./docs/ENGINEERING_COURSE.md)
- ✅ [Grading & Automated Feedback](./docs/GRADING.md)
- 🔌 [API Reference](./docs/API_REFERENCE.md)
- 🗄️ [Database ER Guide](./docs/DATABASE_ER.md)
- 🧠 [Architecture & Request Flow](./docs/ARCHITECTURE.md)
- 🧯 [Troubleshooting](./docs/TROUBLESHOOTING.md)

---

# ✨ What will you build?

## 🎭 AI Characters

- Create custom AI characters.
- Configure name, avatar, chat background, personality, and world setting.
- Assign different voices to different characters.
- Maintain an independent Friend relationship between each user and character.

## 💬 Streaming Chat

- JWT login and token refresh.
- SSE text streaming.
- Persistent message history.
- Recent conversations as short-term context.
- Token-usage persistence.
- `AbortController` to actually terminate the browser SSE request.
- Backend cancellation events to stop generation workers as early as possible.

## 🧠 Long-term Memory

```text
Historical Messages
      +
old Friend.memory
      ↓
MemoryGraph
      ↓
new long-term summary
```

Character identity and user-specific memory are separated:

```text
Character.profile = who the character is
Friend.memory     = what this character remembers about this user
```

## 🧰 LangGraph Agent / Tool Calling

```text
START
  ↓
agent
  ↓
Tool needed?
  ├─ No  → END
  └─ Yes → ToolNode
              ↓
            agent
```

Example tools include:

- current time;
- LanceDB knowledge-base retrieval.

## 📚 RAG

```text
Source documents
      ↓
    Chunk
      ↓
  Embedding
      ↓
   LanceDB
      ↓
  Retrieval
      ↓
source-aware evidence
      ↓
    Agent
```

Retrieval is separated from agent orchestration so it can be evaluated independently. This makes it possible to distinguish **retrieval failures** from **generation failures**.

## 🎙️ Voice

- Browser VAD.
- PCM audio upload.
- WebSocket ASR.
- Parallel LLM text and TTS flow.
- MP3 bytes → Base64 → SSE.
- Continuous browser playback with MediaSource / SourceBuffer.

---

# ⭐ Three AI runtime modes

AiFriends lets learners understand the system before fighting with third-party model services.

| Mode | External services required | Best for learning |
| --- | --- | --- |
| `mock` | None | Vue / Django / JWT / Friend / SSE / DB / CI |
| `text` | Chat model | LLM / LangGraph / Tools / Memory |
| `full` | Chat + Embedding + Speech | RAG / ASR / TTS end-to-end |

## 1. `mock` — recommended first run

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

You do **not** need:

```text
API_KEY
API_BASE
WSS_URL
```

But the request still travels through the real application layers:

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
Message database
```

## 2. `text`

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

Use this mode to learn a real LLM and LangGraph flow without making ASR/TTS a prerequisite for successful chat.

## 3. `full`

Enables Chat + RAG + ASR + TTS.

For backward compatibility, existing deployments without `AI_MODE` still default to `full`. New learners copying `.env.example` start from `mock`.

---

# 🚀 Quick Start

## 1. Clone

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

## 2. Python environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Environment configuration

Windows:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

For your first run, keep:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

## 4. Start Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

### `seed_demo`

Idempotently creates the minimum learning data:

```text
Demo Voice
Reply SystemPrompt
Memory SystemPrompt
```

### `doctor`

Checks what the current AI mode actually requires:

```text
Python
Database
API configuration
SystemPrompt
Voice
LanceDB
VAD assets
```

## 5. Start Vue

Open a new terminal:

```bash
cd frontend
npm ci
npm run dev
```

In development, Vite proxies `/api` and `/media`, reducing first-run CORS and cookie-host friction.

## 6. Send the first message

```text
Register
  ↓
Login
  ↓
Create Character
  ↓
Add Friend
  ↓
Send message
  ↓
Receive a streaming [Mock mode] reply
```

Once this works, move gradually to `text` and then `full`.

---

# 🎙️ Before learning voice features

```bash
cd frontend
npm run setup:vad
```

This prepares the browser VAD / ONNX Runtime static assets from npm dependencies.

Then enable features one at a time:

```env
ENABLE_ASR=true
ENABLE_TTS=true
```

If the environment becomes confusing, run:

```bash
cd backend
python manage.py doctor
```

---

# ✅ Automated feedback

AiFriends currently provides four feedback layers.

## Level 1 — Environment

```bash
cd backend
python manage.py doctor
```

## Level 2 — Course structural grader

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Level 3 — Behavior tests

Backend:

```bash
cd backend
python manage.py test web
```

Frontend:

```bash
cd frontend
npm test
```

## Level 4 — Build / CI

```bash
cd frontend
npm run check
```

Pull requests run GitHub Actions in a clean environment:

```text
Python compile
Chapter 00–20 grader
Migration drift check
Django system check
Backend tests
npm ci
VAD setup
Frontend quality check
Frontend unit tests
Vite production build
Docker learning image build
```

See [GRADING.md](./docs/GRADING.md) for the full grading model.

---

# 🔥 How does one chat message cross the system?

```text
InputField.vue
  ↓
streamApi
  ↓
Authorization: Bearer <JWT>
  ↓
Vite Proxy / Django URL
  ↓
MessageChatView
  ↓
Friend ownership
  ↓
SystemPrompt
+ Character.profile
+ Friend.memory
+ recent Message
  ↓
AI_MODE
  ├─ mock → deterministic local stream
  └─ text/full → CharGraph
                   ↓
                  LLM
                   ↓
                ToolNode
                ├─ time
                └─ RAG retrieval
                     ↓
                source evidence
  ↓
content chunk
  ├──────────────→ SSE text
  └→ optional TTS WebSocket
                   ↓
                MP3 bytes
                   ↓ Base64
                 SSE audio
  ↓
Vue onmessage
  ├─ message bubble
  └─ MediaSource
  ↓
Message persistence
  ↓
periodic Memory update
```

For the deeper explanation, see [ARCHITECTURE.md](./docs/ARCHITECTURE.md) (currently Chinese-first).

---

# 📚 Two-stage curriculum

## Chapters 00–13 — build it first

```text
00 Environment
01 Vue / Router
02 Django / ORM
03 JWT / Pinia / Axios
04 Character CRUD
05 Friend
06 Basic LLM Chat
07 SSE
08 LangGraph / Tool
09 Memory
10 RAG
11 ASR
12 TTS
13 Full Pipeline
```

Goal: **build a complete AI web application independently.**

## Chapters 14–20 — make it reliable

```text
14 Testing / TDD
15 DRF / Serializer / HTTP Status
16 Config / Feature Flag / Provider
17 Async / Cancellation
18 Constraint / Transaction / Security
19 RAG / Memory Evaluation
20 CI / Build / Deploy / Observability
```

Goal: **upgrade a working AI demo into software that can be verified and maintained.**

Start from [Labs](./labs/README.md). The lab prose is currently Chinese-first; code, tests, commands, and acceptance structure are shared.

---

# 🛡️ Security & maintenance

AiFriends has security-sensitive surfaces across:

```text
JWT / refresh cookies
Object-level authorization
File uploads
SSE / WebSocket
LLM Tool Calling
RAG / user data
Third-party AI endpoints
Dependency supply chain
```

Security is treated as part of maintenance, not as an appendix to the course.

- Follow **[SECURITY.md](./SECURITY.md)** for vulnerability reports. Do not publicly disclose an unpatched vulnerability.
- Follow **[CONTRIBUTING.md](./CONTRIBUTING.md)** for normal bugs, tests, docs, and engineering improvements.
- CI uses `mock` mode by default, so contributors do not need to submit real API credentials or spend external-model credits.
- `/api/health/`, `X-Request-ID`, migration drift checks, behavior tests, and the Docker learning build improve diagnosability and regression protection.

> `Dockerfile.learning`, SQLite, Django `runserver`, and development settings are **learning references**, not production-security guarantees. Production deployments still need WSGI/ASGI, HTTPS, PostgreSQL, persistent storage, proper secret management, rate limits, metrics/tracing, and related hardening.

---

# 🧪 RAG Retrieval Evaluation

After configuring real RAG:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

The runner evaluates retrieval separately:

```text
Question
  ↓
Embedding
  ↓
Top-k Retrieval
  ↓
Expected keywords / source
```

This helps distinguish:

```text
Retrieval failed
vs
Evidence was retrieved but the LLM used it poorly
```

That separation is one of the core engineering ideas in Chapter 19.

---

# 🐳 Learning Docker

Use the learning image as a clean-environment reproducibility check:

```bash
docker build -f Dockerfile.learning -t aifriends:learning .
docker run --rm -p 8000:8000 aifriends:learning
```

or:

```bash
docker compose -f compose.learning.yml up --build
```

It intentionally still uses Django `runserver`. Chapter 20 discusses the boundary between a learning image and a production deployment.

---

# 🤝 Contributing

Useful contributions include:

- reproducible bug fixes;
- authentication / authorization / upload / streaming / RAG security improvements;
- regression tests;
- first-run diagnostics and developer tooling;
- fixes for source/documentation drift;
- labs and debugging exercises;
- accessibility / performance / CI / observability / deployment improvements;
- RAG / Memory evaluation cases;
- **English documentation improvements and translations.**

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a large PR.

Minimum checks:

```bash
python scripts/grade.py --chapter 20

cd backend
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py test web

cd ../frontend
npm run check
npm test
npm run build
```

Never commit:

```text
real API keys / JWTs / Django secrets
.env
private conversations
db.sqlite3
runtime LanceDB data
```

---

# 🗺️ Roadmap

The next stage focuses on learning quality, supply-chain security, international accessibility, and production thinking rather than simply adding more beginner content.

## Internationalization / Learning Experience

- [x] Chinese + English repository landing pages
- [ ] Translate the architecture guide and Quick Start into native English docs
- [ ] Translate high-value labs incrementally
- [ ] Stable `course/chXX-start` / `course/chXX-solution` tags
- [ ] Bug Museum based on real historical defects
- [ ] Expected screenshots / GIFs for each chapter
- [ ] More behavioral graders
- [ ] Video index

## Backend / Security

- [ ] Migrate more legacy APIs to Serializers and unified error structures
- [ ] File upload MIME / size / image validation
- [ ] Systematic object-level permissions
- [ ] Refresh-token blacklist / revoke strategy
- [ ] Rate limiting
- [ ] Dependency audit / supply-chain hardening
- [ ] PostgreSQL / concurrent transaction exercises

## AI Engineering

- [ ] Provider Adapter
- [ ] Structured RAG source events + frontend citation UI
- [ ] Generation / Faithfulness evaluation
- [ ] Structured Memory
- [ ] Memory conflict resolution
- [ ] Prompt Injection / Tool permission tests
- [ ] Token / latency dashboard

## Production

- [ ] Production WSGI/ASGI server
- [ ] Nginx / HTTPS
- [ ] Persistent media / object storage
- [ ] PostgreSQL production configuration
- [ ] Structured logging / metrics / tracing
- [ ] Route-level lazy loading / code splitting

---

# 📄 License

AiFriends is open source under the **MIT License**. See [LICENSE](./LICENSE).

---

## The most important learning principle

Do not debug all of this on day one:

```text
Vue + Django + JWT + SSE + LangGraph + RAG + Memory + ASR + TTS + Docker
```

Use this order instead:

> **Run Mock first → understand one request → rebuild it yourself → prove it with tests → enable complexity one capability at a time.**
