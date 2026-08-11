# AiFriends English Quick Start

🌐 **Language:** [简体中文学习中心](./README.md) | **English**

> Goal: get the real Vue + Django + JWT + Friend + SSE + Message-persistence path running **without any external AI API key**.

For your first run, use `AI_MODE=mock`. Do not begin by configuring LLM, embedding, ASR, and TTS providers at the same time.

---

# 1. What you will prove

By the end of this guide, you should be able to:

```text
Open the Vue app
  ↓
Register / log in
  ↓
Create a Character
  ↓
Create or open a Friend relationship
  ↓
Send a message
  ↓
Receive a streamed mock reply over SSE
  ↓
Confirm the Message was persisted by Django
```

This is intentionally a real application path with a deterministic local AI response.

---

# 2. Prerequisites

Install:

- Git
- Python 3.12 or 3.13
- Node.js compatible with `frontend/package.json`
- npm

Verify:

```bash
git --version
python --version
node --version
npm --version
```

On some Windows systems, use `py --version` if `python` is not available.

---

# 3. Clone the repository

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

The two main runtime applications are separate:

```text
backend/   Django + DRF
frontend/  Vue 3 + Vite
```

Python dependencies are managed by `requirements.txt`; JavaScript dependencies are managed by `frontend/package.json` and its lockfile.

---

# 4. Create a Python virtual environment

From the repository root:

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

Install backend dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

A useful sanity check:

```bash
python -c "import django; print(django.get_version())"
```

---

# 5. Create `.env`

Copy the example file.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

For the first run, keep the learning defaults:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

In this mode you do **not** need real values for:

```text
API_KEY
API_BASE
WSS_URL
```

Never commit a real `.env` file or credentials.

---

# 6. Start Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

## What these commands do

### `migrate`

Creates or updates the SQLite schema.

### `seed_demo`

Idempotently prepares learning data required by the project, including demo prompt/voice records used by the tutorial flow.

### `doctor`

Checks the environment according to the selected runtime mode. In `mock` mode, external LLM/RAG/speech credentials are not required.

### `runserver`

Starts Django, normally at:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

---

# 7. Start Vue

Open a second terminal at the repository root:

```bash
cd frontend
npm ci
npm run dev
```

Vite normally starts at:

```text
http://localhost:5173
```

The development server proxies `/api` and `/media` to Django, reducing local CORS and cookie-host friction.

Open the Vite URL in your browser.

---

# 8. Run the first end-to-end flow

In the browser:

```text
Register
  ↓
Log in
  ↓
Create a Character
  ↓
Add/open the Character as a Friend
  ↓
Open chat
  ↓
Send a message
```

You should see a streamed deterministic response indicating Mock mode.

Even though no external model is called, the request still crosses the real application layers:

```text
Vue InputField
  ↓
JWT-authenticated request
  ↓
Django MessageChatView
  ↓
Friend ownership check
  ↓
StreamingHttpResponse / SSE
  ↓
Vue incremental update
  ↓
Message persistence
```

That makes Mock mode useful for Chapters 00–07, regression tests, CI, and debugging.

---

# 9. Verify with machine feedback

## Backend

```bash
cd backend
python manage.py doctor
python manage.py check
python manage.py test web
```

## Course structure

From the repository root:

```bash
python scripts/grade.py --chapter 7
python scripts/grade.py --chapter 13
python scripts/grade.py --chapter 20
```

## Frontend

```bash
cd frontend
npm run check
```

Do not use “the page looks fine” as your only acceptance criterion.

---

# 10. Move from Mock to a real text model

Once the local flow is stable, configure your OpenAI-compatible chat provider in `.env`, then switch to:

```env
AI_MODE=text
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

Configure the relevant values, for example:

```env
API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

Run again:

```bash
cd backend
python manage.py doctor
```

Do not enable RAG and speech until basic real-text chat works.

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

# 11. Before learning voice

Prepare the browser VAD / ONNX Runtime assets once:

```bash
cd frontend
npm run setup:vad
```

Then enable speech features only after you have configured the corresponding provider/WebSocket service:

```env
ENABLE_ASR=true
ENABLE_TTS=true
```

Re-run:

```bash
cd backend
python manage.py doctor
```

---

# 12. Common first-run failures

## `ModuleNotFoundError`

Check that the virtual environment is activated and that `pip install -r requirements.txt` completed successfully.

## `npm` is not recognized

Node.js is missing or the terminal has not picked up the new PATH.

## Django starts but the frontend cannot call the API

Check:

```text
Django terminal
Vite terminal
Browser DevTools → Network
```

The development frontend should call same-origin `/api/...` routes through the Vite proxy.

## Registration/login returns 401 or another auth error

Treat this as an authentication problem first, not an LLM problem.

## Chat works in Mock mode but fails in Text mode

Run:

```bash
python manage.py doctor
```

Then verify API key, API base URL, and chat-model name independently.

## Voice fails while text works

That is a useful isolation result. Check VAD assets, ASR/TTS feature flags, provider WebSocket configuration, and voice data without changing the text-chat path.

---

# 13. What to read next

Recommended English path:

1. [Chapter 00 — Environment](../labs/en/chapter-00-environment.md)
2. [Chapter 06 — Minimal LLM Chat](../labs/en/chapter-06-basic-chat.md)
3. [Chapter 07 — SSE Streaming](../labs/en/chapter-07-sse.md)
4. [Chapter 08 — LangGraph Tool Calling](../labs/en/chapter-08-langgraph-tools.md)
5. [Chapter 10 — RAG + LanceDB](../labs/en/chapter-10-rag.md)
6. [Chapter 13 — Full-System Capstone](../labs/en/chapter-13-capstone.md)
7. [English Architecture Guide](./ARCHITECTURE_EN.md)

For the complete Chinese-first Chapter 00–20 curriculum, see [Labs](../labs/README.md).

---

Return to the [English Learning Hub](./README_EN.md).
