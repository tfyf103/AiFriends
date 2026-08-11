# 🤖 AiFriends

[![AiFriends CI](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml/badge.svg)](https://github.com/tfyf103/AiFriends/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20AiFriends-2ea44f)](https://app8056.acapp.acwing.com.cn/)

🌐 **Language / 语言:** [简体中文](./README.md) | **English**

> **Build an AI companion with characters, long-term memory, RAG, agents, and voice — then learn how to test, secure, maintain, and ship it.**
>
> An open-source, project-based full-stack AI curriculum and reference application for learning how modern AI products are actually engineered and maintained.

AiFriends uses **Vue 3 + Django + DRF + JWT + LangChain + LangGraph + LanceDB + SSE + WebSocket** to turn a real AI application into a reproducible, testable, progressively engineered learning path.

This is not a “call one LLM API and print the answer” demo. It connects browser UI, authentication, persistence, streaming protocols, agents, RAG, long-term memory, ASR/TTS, automated tests, data integrity, security boundaries, CI, and build workflows in one repository.

> **English documentation status:** the core curriculum and high-value maintainer path are now internationalized. English learners can complete **Chapters 00–20**, study real Git-history engineering archaeology, use the maintained architecture/API/database references, follow a bilingual terminology baseline, inspect real screenshots/GIFs, and run a Browser E2E example. CI guards core bilingual/source structure against silent drift.

---

## 30-second project snapshot

| Area | Current status |
| --- | --- |
| License | **MIT** |
| Maintenance | **Active development**, primarily maintained by `@tfyf103` |
| Languages | **Chinese + English** project and core learning paths |
| Live demo | **[Open the real deployment](https://app8056.acapp.acwing.com.cn/)** |
| First-run barrier | `AI_MODE=mock` runs the core Web/SSE flow with **zero API keys** |
| Curriculum | Chapters **00–20**, fully available as English Labs |
| Automated feedback | Django tests + Node tests + Browser E2E + structural grader + i18n/source drift + GitHub Actions |
| AI stack | LangGraph Agent / Tool Calling / Memory / RAG / ASR / TTS |
| Engineering stack | Serializers / cancellation / migrations / Health / Request-ID / Docker learning image |
| English references | Quick Start / Git History / Architecture / Engineering / API / ER / Troubleshooting |
| Security | [SECURITY.md](./SECURITY.md) |
| Contributing | [CONTRIBUTING.md](./CONTRIBUTING.md) |

> **Project goal:** help learners go beyond “getting an AI demo to work” and understand why the system is designed this way, how to verify it, how to maintain it, and how to evolve it toward reliable software engineering.

---

# 🌐 Live Demo

**Production deployment:** [https://app8056.acapp.acwing.com.cn/](https://app8056.acapp.acwing.com.cn/)

> These are not mock or generated screenshots. On **2026-08-11**, a GitHub-hosted Ubuntu runner with Playwright Chromium visited the real deployment from an independent public network. Verification was **read-only**: no test account, Character, Friend, or chat data was created or modified.

Verified public routes:

```text
/                         → HTTP 200
/user/account/login       → HTTP 200
/user/account/register    → HTTP 200
/user/space/6             → HTTP 200
```

## Homepage — discover public AI characters

[![AiFriends live homepage](./docs/assets/live-demo/homepage.png)](https://app8056.acapp.acwing.com.cn/)

The deployed homepage loads real public Character cards and profiles, demonstrating the running discovery layer rather than a static README concept.

## Login and registration

<p align="center">
  <img src="./docs/assets/live-demo/login.png" alt="AiFriends live login page" width="49%" />
  <img src="./docs/assets/live-demo/register.png" alt="AiFriends live register page" width="49%" />
</p>

## Public user space

[![AiFriends live public profile](./docs/assets/live-demo/public-profile.png)](https://app8056.acapp.acwing.com.cn/user/space/6)

> Screenshots are real production snapshots captured on **2026-08-11**. Public Characters, profile data, and deployed assets can evolve over time. See [Live Demo Verification](./docs/LIVE_DEMO.md) for the capture method and scope.

## Real walkthrough GIF

![AiFriends real production walkthrough](./docs/assets/live-demo/walkthrough.gif)

The GIF is reproducibly built only from the real production PNGs above; it is not generated UI. See the [Screenshots & GIF Guide](./docs/SCREENSHOTS.md) for visual-evidence rules.

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

AiFriends bridges that engineering gap with a **code-first, reproducible, experiment-driven learning path with automated feedback**.

The tutorial and maintained application live in the same repository. Learners inspect real runtime paths, Git history, tests, data migrations, CI, security boundaries, and deployment trade-offs instead of switching to a separate toy implementation.

The project started in the Chinese AI learning community and now offers a complete English core curriculum for developers worldwide.

---

# 🌍 English learning path

```text
README_EN
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
Chapter 13 Full-System Capstone
  ↓
Chapter 14 → 15 → 16 → 17 → 18 → 19 → 20
  ↓
Architecture / API / Database / Troubleshooting
  ↓
Contribute fixes, tests, evaluations, docs, or translations
```

## English-first resources

- 🌍 [English Learning Hub](./docs/README_EN.md)
- 🚀 [English Quick Start](./docs/QUICK_START_EN.md)
- 🧭 [English Git-history Rebuild](./docs/COURSE_REBUILD_EN.md)
- 🧪 [English Labs: Chapter 00–20](./labs/en/README.md)
- 🧠 [English Architecture Guide](./docs/ARCHITECTURE_EN.md)
- 🏗️ [English Engineering Course: Chapter 14–20](./docs/ENGINEERING_COURSE_EN.md)
- 🔌 [English API Reference](./docs/API_REFERENCE_EN.md)
- 🗄️ [English Database / ER Guide](./docs/DATABASE_ER_EN.md)
- 🧯 [English Troubleshooting Guide](./docs/TROUBLESHOOTING_EN.md)
- 🌐 [Bilingual Engineering Glossary](./docs/BILINGUAL_GLOSSARY.md)
- 🖼️ [Screenshots & GIF Guide](./docs/SCREENSHOTS.md)
- 🧪 [Browser E2E example](./e2e/README.md)
- ✅ [Grading & Automated Feedback](./docs/GRADING.md)
- 🛡️ [Security Policy](./SECURITY.md)
- 🤝 [Contributing Guide](./CONTRIBUTING.md)

## Chinese resources

- 📘 [中文学习中心](./docs/README.md)
- 🚀 [零基础完整教程](./docs/BEGINNER_TUTORIAL.md)
- 🧭 [沿真实 Git 历史重建](./docs/COURSE_REBUILD.md)
- 🧪 [中文 Labs: Chapter 00–20](./labs/README.md)
- 🏗️ [工程进阶课程](./docs/ENGINEERING_COURSE.md)
- 🔌 [API Reference](./docs/API_REFERENCE.md)
- 🗄️ [数据库 ER 图](./docs/DATABASE_ER.md)
- 🧯 [排错手册](./docs/TROUBLESHOOTING.md)

Real Git-history engineering archaeology is now available in both languages through `COURSE_REBUILD.md` and `COURSE_REBUILD_EN.md`. Remaining internationalization work is ongoing maintenance quality rather than a missing core learning path.

---

# ✨ What will you build?

## 🎭 AI Characters

- Create custom AI characters.
- Configure name, avatar, chat background, personality, and world setting.
- Assign voices to Characters.
- Maintain an independent Friend relationship between each user and Character.

## 💬 Streaming Chat

- JWT login and refresh.
- SSE text streaming.
- Persistent Message history.
- Recent conversations as short-term context.
- Token-usage persistence.
- `AbortController` to terminate the browser stream.
- Backend cancellation events to stop workers as early as possible.

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

```text
Character.profile = who the Character is
Friend.memory     = what this Character remembers about this user
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

Example tools include current-time lookup and LanceDB knowledge retrieval.

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

Retrieval is separated from Agent orchestration so it can be evaluated independently. This lets maintainers distinguish **retrieval failures** from **generation failures**.

## 🎙️ Voice

- Browser VAD.
- PCM audio upload.
- WebSocket ASR.
- Parallel LLM text and TTS flow.
- MP3 bytes → Base64 → SSE.
- Browser playback with MediaSource / SourceBuffer.

---

# ⭐ Three AI runtime modes

| Mode | External services | Best for |
| --- | --- | --- |
| `mock` | None | Vue / Django / JWT / Friend / SSE / DB / CI |
| `text` | Chat model | LLM / LangGraph / Tools / Memory |
| `full` | Chat + Embedding + Speech | RAG / ASR / TTS end-to-end |

## `mock` — recommended first run

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

No `API_KEY`, `API_BASE`, or `WSS_URL` is required for the core learning path.

The request still goes through real application layers:

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

## `text`

```env
AI_MODE=text
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

Use a real LLM without making speech a prerequisite.

## `full`

Enable the full Chat + RAG + ASR + TTS path, subject to feature flags and provider configuration.

---

# 🚀 Quick Start

For the maintained step-by-step guide, use **[docs/QUICK_START_EN.md](./docs/QUICK_START_EN.md)**.

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

```bash
pip install -r requirements.txt
```

## 3. Environment

Windows:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Keep the first run in Mock mode.

## 4. Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

## 5. Vue

Open another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Vite proxies `/api` and `/media` during development.

## 6. First message

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
Receive streaming Mock reply
```

Then move gradually to `text`, RAG, ASR, TTS, and `full`.

---

# ✅ Automated feedback

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

## Backend tests

```bash
cd backend
python manage.py test web
```

## Frontend checks

```bash
cd frontend
npm run check
```

Pull requests run GitHub Actions for:

```text
Python compile
internationalization/documentation drift check
live-demo GIF drift check
Chapter 00–20 grader
migration drift
Django check/tests
npm ci
VAD setup
frontend quality/tests/build
Chromium Browser E2E in AI_MODE=mock
learning Docker image build
```

---

# 🔥 One chat message across the system

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
SystemPrompt + Character.profile + Friend.memory + recent Message
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
  ├→ SSE text
  └→ optional TTS WebSocket → MP3 → Base64 → SSE audio
  ↓
Vue UI / MediaSource
  ↓
Message persistence
  ↓
periodic Memory update
```

Deep dive: [English Architecture Guide](./docs/ARCHITECTURE_EN.md).

---

# 📚 Chapter 00–20 curriculum

## Stage 1 — Build it

```text
00 Environment
01 Vue / Router
02 Django / ORM
03 JWT / Pinia / Axios
04 Character CRUD
05 Friend
06 Basic LLM Chat
07 SSE
08 LangGraph / Tool Calling
09 Long-Term Memory
10 RAG
11 ASR
12 Streaming TTS
13 Full-System Capstone
```

## Stage 2 — Engineer it

```text
14 Testing / TDD
15 DRF / Serializer / HTTP Status
16 Config / Feature Flags / Providers
17 Async / Streaming / Cancellation
18 Constraints / Transactions / Security
19 RAG / Memory Evaluation
20 CI / Build / Deploy / Observability
```

All chapters are available in [English Labs](./labs/en/README.md).

---

# 🛡️ Security & maintenance

AiFriends spans security-sensitive surfaces:

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

- Follow [SECURITY.md](./SECURITY.md) for suspected vulnerabilities.
- Follow [CONTRIBUTING.md](./CONTRIBUTING.md) for normal bugs, tests, docs, and improvements.
- CI uses Mock mode so contributors do not need real model credentials.
- `/api/health/`, `X-Request-ID`, migration checks, tests, and learning Docker improve diagnosability and regression protection.

> `Dockerfile.learning`, SQLite, Django `runserver`, and development settings are **learning references**, not production-security guarantees.

---

# 🧪 RAG Retrieval Evaluation

After configuring real RAG:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

This evaluates retrieval separately from generation and checks expected evidence/source behavior.

Learn more in:

- [Chapter 10 RAG](./labs/en/chapter-10-rag.md)
- [Chapter 19 RAG / Memory Evaluation](./labs/en/chapter-19-rag-memory-eval.md)

---

# 🐳 Learning Docker

```bash
docker build -f Dockerfile.learning -t aifriends:learning .
docker run --rm -p 8000:8000 aifriends:learning
```

or:

```bash
docker compose -f compose.learning.yml up --build
```

Chapter 20 explains why the learning image is different from a production deployment.

---

# 🤝 Contributing

Useful contributions include:

- reproducible bug fixes;
- authentication / authorization / upload / streaming / RAG security improvements;
- regression tests and browser E2E;
- first-run diagnostics;
- documentation/source drift fixes;
- labs and debugging exercises;
- accessibility / performance / CI / observability / deployment improvements;
- RAG / Memory evaluation cases;
- **English and Chinese documentation synchronization and translation quality improvements.**

Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a large PR.

Never commit real secrets, JWTs, private conversations, or local private knowledge-base data.

---

# 🗺️ Roadmap

## Internationalization / Learning Experience

- [x] Chinese + English repository landing pages
- [x] English Learning Hub
- [x] English Quick Start
- [x] English Architecture Guide
- [x] **Complete English Chapter 00–20 Labs**
- [x] English Engineering Course overview
- [x] English API Reference
- [x] English Database / ER Guide
- [x] English Troubleshooting Guide
- [x] Explicitly welcome bilingual documentation contributions
- [x] English `COURSE_REBUILD` / real Git-history engineering archaeology
- [x] Structural CI guard for core bilingual docs and important source sentinels
- [x] First real bilingual Live Demo screenshots + reproducible walkthrough GIF
- [ ] Add focused screenshots / GIFs / expected results to more high-value chapters
- [x] Bilingual engineering terminology baseline and contribution rules
- [ ] Continue accessibility-language improvements

## Learning Quality

- [ ] Stable `course/chXX-start` / `course/chXX-solution` tags
- [ ] Bug Museum based on real historical defects
- [ ] More behavioral graders
- [x] Browser E2E in Mock mode (registration / protected route / reload restoration)
- [ ] Video index

## Backend / Security

- [ ] Migrate more legacy APIs to Serializers and unified errors
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
- [ ] Structured Memory + provenance/conflict handling
- [ ] Prompt Injection / Tool permission tests
- [ ] Token / latency dashboard

## Production

- [ ] Production WSGI/ASGI server
- [ ] Nginx / HTTPS
- [ ] Persistent media / object storage
- [ ] PostgreSQL production configuration
- [ ] Structured logging / metrics / tracing
- [ ] Route-level lazy loading / code splitting / bundle budget

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
