# Chapter 00 Lab: From a Clean Machine to a Running Frontend and Backend

🌐 **Language:** [简体中文](../chapter-00-environment.md) | **English**

## Goal

Do not write business logic in this chapter. Complete one thing only:

> **Build a development environment that a new learner can reproduce.**

When you finish, you should be able to run both:

```text
Vite:   http://localhost:5173
Django: http://127.0.0.1:8000
```

For the current project, the recommended first run uses `AI_MODE=mock`, so you do not need an external model provider yet.

---

## Starting point

Read first:

- [English Quick Start](../../docs/QUICK_START_EN.md)
- the repository [`.env.example`](../../.env.example)

Install:

- Git
- Python 3.12 or 3.13
- Node.js compatible with `frontend/package.json`
- VS Code or another editor of your choice

---

## TODO 1: Prove the tools actually work

Run:

```bash
git --version
python --version
node --version
npm --version
```

### Acceptance

- [ ] All four commands execute successfully.
- [ ] You know that Windows may use `py` if `python` is unavailable.
- [ ] You understand that Node/npm are frontend tools, not Python packages.

Do not continue based on “I think I installed it.” Record the versions.

---

## TODO 2: Clone the repository and identify responsibilities

```bash
git clone https://github.com/tfyf103/AiFriends.git
cd AiFriends
```

Do not immediately start every process. First explain the role of:

```text
backend/
frontend/
docs/
labs/
requirements.txt
.env.example
```

### Acceptance

You can explain:

> `requirements.txt` manages the Python environment, while `frontend/package.json` manages the JavaScript environment. They are separate runtimes.

---

## TODO 3: Create a Python virtual environment

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

### Required observation

Run this before and after activating the virtual environment:

```bash
python -c "import sys; print(sys.executable)"
```

Observe how the Python executable path changes.

### Acceptance

- [ ] You can explain why a virtual environment prevents dependency conflicts between projects.
- [ ] `python -c "import django; print(django.get_version())"` works.

---

## TODO 4: Create the environment configuration

Copy the example file.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

For the first run, keep:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

Understand the external-provider variables even though Mock mode does not require real values:

```text
API_KEY   = credential for model/provider access
API_BASE  = OpenAI-compatible HTTP endpoint
WSS_URL   = speech WebSocket endpoint for ASR/TTS
```

### Security experiment

Run:

```bash
git status
```

Verify that the real `.env` is not prepared for commit.

- [ ] `.env` is not tracked.
- [ ] `.env.example` is safe to commit because it contains placeholders only.
- [ ] You can explain why real API keys never belong in README files, Issues, screenshots, or frontend JavaScript.

---

## TODO 5: Start Django

```bash
cd backend
python manage.py migrate
python manage.py seed_demo
python manage.py doctor
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000
```

### What each command proves

```text
migrate    → database schema can be prepared
seed_demo  → tutorial data can be created idempotently
doctor     → selected runtime mode has required dependencies/config
runserver  → Django can serve requests
```

### Deliberate failure experiment

Stop Django, then refresh or trigger a frontend request.

Observe the browser and terminal behavior.

Explain why:

> A frontend error is not the same thing as “Django is down,” and “Django is down” is not an LLM problem.

---

## TODO 6: Start Vue

Open a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Visit:

```text
http://localhost:5173
```

The development server proxies `/api` and `/media` to Django, so the browser-facing development flow does not require you to solve cross-origin configuration before learning the application.

### Acceptance

- [ ] Vite is running.
- [ ] Django is running in another terminal.
- [ ] Browser DevTools → Network can show requests to `/api/...`.

---

## TODO 7: Complete one Mock-mode chat

Use the UI to:

```text
Register
  ↓
Log in
  ↓
Create a Character
  ↓
Open/add a Friend relationship
  ↓
Send a chat message
  ↓
Receive a streamed Mock response
```

### Why this matters

No external LLM is called, but the request still exercises the real application path:

```text
Vue
 ↓
JWT
 ↓
Django
 ↓
Friend ownership
 ↓
SSE
 ↓
Vue streaming update
 ↓
Message persistence
```

This is much more useful than a fake static page because it proves the project skeleton itself works.

---

## Reference mental model

There is no single “code answer” for this chapter. The correct result is that you can separate:

```text
System tools
├── Git
├── Python
└── Node

Python project environment
├── .venv
└── requirements.txt

Frontend environment
├── node_modules
├── package.json
└── package-lock.json

Runtime processes
├── Django :8000
└── Vite   :5173

Runtime mode
└── AI_MODE=mock
```

---

## Common errors

### `ModuleNotFoundError`

Check that the virtual environment is active and that `pip install -r requirements.txt` succeeded.

### `npm` is not a command

Node.js is missing or your terminal has not refreshed its PATH.

### Port already in use

Do not randomly kill processes. First identify what owns port 5173 or 8000, then decide whether to stop it or use another port.

### `.env` exists but the backend still behaves incorrectly

Check the filename, working directory, environment loading, and `python manage.py doctor` output.

### Chat fails in Mock mode

Do not debug model credentials. Inspect:

```text
Network
JWT/auth
Django traceback
Friend ownership
SSE response
```

Mock mode intentionally removes external AI providers from this failure space.

---

## Challenge

Create a local `MY_SETUP_NOTES.md` file. Do not put secrets in it.

Record:

- operating system;
- Python version;
- Node version;
- the first error you encountered;
- the evidence you used to locate it;
- the fix;
- one command that proves the setup is healthy.

If you can move to a new machine and rebuild the project using your own notes, you have completed Chapter 00.

---

Next: [Chapter 06 — Minimal LLM Chat](./chapter-06-basic-chat.md)
