# AiFriends Troubleshooting Guide

🌐 **Language:** [简体中文](./TROUBLESHOOTING.md) | **English**

> The most important beginner skill is not “never seeing errors.” It is learning to identify **which layer is failing** before changing code.

---

# 1. Start by locating the layer

When something fails, ask in this order:

```text
A. Python / virtual environment?
B. Node / npm environment?
C. Django startup/config?
D. Vue/Vite startup?
E. Vite proxy / CORS / cookies?
F. JWT authentication/refresh?
G. Database/migrations?
H. AI_MODE / feature flags?
I. LLM provider?
J. LangGraph Tool Calling?
K. LanceDB / Embedding / RAG?
L. ASR / microphone / PCM?
M. TTS / SSE audio / MediaSource?
N. Build / Vite manifest / Docker?
```

Do not see “chat failed” and immediately rewrite LangGraph.

A better debugging order is:

```text
reproduce
  ↓
identify layer
  ↓
collect evidence
  ↓
make one small change
  ↓
re-test
```

---

# 2. Run the project doctor first

Current AiFriends includes:

```bash
cd backend
python manage.py doctor
```

`doctor` checks the requirements implied by the selected runtime mode/features, including concepts such as:

```text
Python version
Database
AI_MODE
API_KEY / API_BASE when needed
WSS_URL when speech is enabled
SystemPrompt rows
Voice readiness
LanceDB storage
VAD assets
```

If you are unsure whether the environment is ready, use this before manually guessing through 10 files.

---

# 3. `python` command does not exist

Try:

```bash
python --version
py --version
python3 --version
```

Typical patterns:

```text
Windows → `py` may exist even if `python` does not
macOS/Linux → `python3` may be the configured command
```

Use the working command consistently in later steps.

---

# 4. Django 6 fails to install

Check:

```bash
python --version
```

AiFriends currently uses Django 6.x and expects a modern Python version. For the course, Python 3.12/3.13 is the safest documented path.

If you are on Python 3.10/3.11, upgrade Python instead of randomly downgrading project dependencies.

---

# 5. `ModuleNotFoundError: dotenv`

Install the locked requirements in the active virtual environment:

```bash
pip install -r requirements.txt
```

Verify:

```bash
python -c "from dotenv import load_dotenv; print('ok')"
```

If this works in one terminal but not another, compare which Python executable each terminal uses.

---

# 6. Dependencies are installed, but Django still cannot import them

Most common cause: wrong Python/virtual environment.

Activate:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Inspect:

```bash
python -c "import sys; print(sys.executable)"
```

Windows can also use:

```cmd
where python
```

macOS/Linux:

```bash
which python
```

The path should point into `.venv`.

---

# 7. PowerShell refuses to activate the virtual environment

For the current shell session you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

then:

```powershell
.\.venv\Scripts\Activate.ps1
```

Understand what policy you are changing; do not globally weaken script security just to get through a tutorial.

---

# 8. `node` / `npm` does not exist

Check:

```bash
node -v
npm -v
```

Install a Node version compatible with `frontend/package.json`.

Do not treat Python/npm dependencies as one environment. AiFriends has two runtimes:

```text
backend  → Python
frontend → Node.js
```

---

# 9. `npm ci` / install reports an engine mismatch

Run:

```bash
node -v
```

Upgrade Node when required.

Avoid starting with:

```bash
npm install --force
```

because forcing an unsupported engine may create a harder-to-debug build/runtime mismatch.

---

# 10. `manage.py` not found

You are probably in the wrong directory.

Correct:

```bash
cd AiFriends/backend
python manage.py migrate
```

Confirm the current directory contains:

```text
manage.py
```

---

# 11. Django port 8000 is already in use

You may temporarily run:

```bash
python manage.py runserver 8001
```

But current Vite development proxy targets the default Django host/port.

If you change the backend port, update the relevant proxy/development configuration rather than editing every API call in Vue.

---

# 12. Vite port 5173 is already in use

Vite may choose another port.

The current development design uses a Vite proxy for `/api` and `/media`, which reduces cross-origin/cookie problems when the expected dev host is used.

If the frontend host/port changes, check:

```text
Vite dev server URL
Django CORS allowed origins
cookie/site behavior
proxy target
```

---

# 13. Browser reports CORS

First confirm whether your request should actually be going through the Vite proxy.

Current recommended development path:

```text
Browser → Vite localhost:5173
             ↓ /api, /media
          Django 127.0.0.1:8000
```

If you bypass the proxy or change origins, inspect Django CORS configuration.

Remember:

```text
localhost
```

and:

```text
127.0.0.1
```

are not the same origin/host identity in browser security rules.

---

# 14. Page loads, but API returns 404

Open:

```text
DevTools → Network
```

Check the exact Request URL.

Backend route table:

```text
backend/web/urls.py
```

For chat, for example:

```text
/api/friend/message/chat/
```

Also check the trailing slash. Django route behavior is often slash-sensitive.

---

# 15. API returns 401 Unauthorized

Determine which case applies:

```text
not logged in?
Authorization header missing?
access token expired/invalid?
refresh cookie missing/expired?
refresh flow failed?
```

DevTools → Network → Request Headers should show:

```http
Authorization: Bearer <access-token>
```

Frontend files:

```text
frontend/src/stores/user.js
frontend/src/js/http/api.js
frontend/src/js/http/authRefresh.js
```

---

# 16. Normal Axios refresh works, but SSE gets 401

Streaming uses:

```text
frontend/src/js/http/streamApi.js
```

Current code intentionally shares refresh logic with Axios via:

```text
frontend/src/js/http/authRefresh.js
frontend/src/js/utils/singleFlight.js
```

Expected flow:

```text
SSE open → 401
  ↓
refreshAccessToken()
  ↓
new access written to Pinia
  ↓
restart stream
  ↓
rebuild Authorization header
```

A historical bug refreshed successfully but reconnected using stale access state. If you reproduce that symptom, make sure you did not reintroduce separate refresh logic into `streamApi.js`.

---

# 17. Login/register succeeds, but UI still thinks the user is logged out

Inspect Pinia:

```text
frontend/src/stores/user.js
```

and router guards:

```text
frontend/src/router/index.js
```

Common issue:

> API authentication succeeded, but app state was never updated/restored.

On a browser reload, remember that in-memory Pinia state resets. The app must restore access through the refresh cookie and then load user information.

---

# 18. Many requests trigger many refresh calls

Inspect:

```text
frontend/src/js/utils/singleFlight.js
frontend/src/js/http/authRefresh.js
```

Desired behavior:

```text
A 401 ─┐
B 401 ─┼→ one refresh Promise
C 401 ─┘
```

Run:

```bash
cd frontend
npm test
```

to verify the single-flight helper still satisfies its concurrency tests.

---

# 19. Django 500 Internal Server Error

Do not guess from the browser alone.

Read the Django terminal traceback.

Start at the bottom and identify:

```text
exception type
message
your source file
line number
```

Then trace back to request input/config/database state.

Example:

```text
KeyError: friend_id
```

means you should inspect the actual payload before touching model/provider code.

---

# 20. `no such table`

Usually migrations were not applied:

```bash
cd backend
python manage.py migrate
```

If you changed models in your branch:

```bash
python manage.py makemigrations
python manage.py migrate
```

Before opening a PR, current CI also checks migration drift:

```bash
python manage.py makemigrations --check --dry-run
```

---

# 21. Friend duplicates or `IntegrityError` on Friend creation

Current `main` has a database uniqueness constraint:

```text
(me, character) must be unique
```

and the View uses `get_or_create()`.

If duplicate creation reaches the database under a race, the constraint may raise an integrity error rather than allow invalid data.

This is a sign that API-level race/error handling may need improvement—not that the constraint should be removed.

---

# 22. Uploaded avatar/background cannot be displayed

Current development media flow is proxied through Vite where appropriate.

Check:

```text
MEDIA_URL
MEDIA_ROOT
backend/media/
Vite /media proxy
Django DEBUG media serving
actual file exists
```

Do not assume the database stores the image bytes; Django usually stores a file path/reference while the file lives in media storage.

---

# 23. `.env` exists, but configuration is still missing

Make sure the file is actually named:

```text
.env
```

not:

```text
.env.txt
```

Then run:

```bash
cd backend
python manage.py doctor
```

Current settings include more than the original three provider variables, for example:

```text
AI_MODE
ENABLE_RAG
ENABLE_ASR
ENABLE_TTS
API_KEY
API_BASE
WSS_URL
CHAT_MODEL
MEMORY_MODEL
EMBEDDING_MODEL
EMBEDDING_DIMENSIONS
ASR_MODEL
TTS_MODEL
```

The required subset depends on mode/features.

---

# 24. Mock mode still tries to call a real model

Check:

```env
AI_MODE=mock
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false
```

Then run:

```bash
python manage.py doctor
python manage.py test web
```

Mock chat should use deterministic local streaming and should not require external model credentials.

If you see provider network traffic, inspect branching in the chat/config layer.

---

# 25. Real text chat fails because speech config is missing

Use:

```env
AI_MODE=text
ENABLE_ASR=false
ENABLE_TTS=false
```

Text mode should not require a speech WebSocket just to chat.

If it does, check whether TTS/ASR code has accidentally become a mandatory dependency again.

---

# 26. LLM provider returns 401 / 403

This is different from Django JWT 401.

Check provider settings:

```text
API_KEY
API_BASE
CHAT_MODEL / MEMORY_MODEL
account/model permission
```

Use `doctor` for local configuration gaps, then inspect the provider response for account/model authorization errors.

---

# 27. `model not found`

OpenAI-compatible protocol does **not** mean universal model names.

Check each configured capability:

```text
CHAT_MODEL
MEMORY_MODEL
EMBEDDING_MODEL
ASR_MODEL
TTS_MODEL
```

Provider support can differ for:

```text
model names
tool calling
stream metadata
embedding dimensions
speech protocols
```

Change configuration before editing business Views.

---

# 28. Chat works, Embedding fails

Chat and Embedding are separate model calls.

Inspect:

```text
backend/web/documents/utils/custom_embeddings.py
backend/web/ai/config.py
```

Check:

```text
EMBEDDING_MODEL
EMBEDDING_DIMENSIONS
API_BASE
provider dimension support
```

A provider can support chat while not supporting the configured embedding model/parameters.

---

# 29. RAG reports missing LanceDB table/storage

Create a local knowledge source such as:

```text
backend/web/documents/data.txt
```

then build the index using the project helper from Django context.

Afterwards check:

```text
backend/web/documents/lancedb_storage
```

If RAG is not part of your current learning mode, keep:

```env
ENABLE_RAG=false
```

rather than forcing every beginner to build a vector store.

---

# 30. `data.txt` is missing from Git

That can be intentional. Local/private knowledge content should not automatically be committed.

Create your own:

```text
backend/web/documents/data.txt
```

Never add private customer/user documents just because the tutorial uses a local file example.

---

# 31. RAG has data, but Agent never calls the Tool

Inspect:

```text
backend/web/views/friend/message/chat/graph.py
backend/web/documents/retrieval.py
ENABLE_RAG
```

Check:

- RAG tool is actually registered;
- the Tool description matches the knowledge domain;
- the model supports Tool Calling;
- the user question plausibly requires the knowledge base.

Do not force every question through RAG if the tool is meant to be conditional.

---

# 32. RAG answers are wrong — retrieval or generation?

Run retrieval separately:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

Then inspect the returned Documents before blaming the LLM.

Separate:

```text
Retrieval failure → wrong/missing chunks
Generation failure → good evidence, poor final answer
```

This distinction is one of the core Chapter 19 practices.

---

# 33. RAG source exposes an absolute server path

Current retrieval helpers are designed to normalize source labels.

Inspect:

```text
backend/web/documents/retrieval.py
```

Expected external source label:

```text
data.txt
```

not:

```text
/home/private/server/.../data.txt
```

If you add new loaders/indexers, preserve this privacy property.

---

# 34. Tool executes, but there is no final natural-language answer

Check the LangGraph loop:

```text
agent
  ↓ tool_calls
tools
  ↓ ToolMessage
agent
  ↓ final answer
```

The important edge is conceptually:

```text
tools → agent
```

Tool output normally goes back to the model before being presented as a final answer.

---

# 35. LangGraph `tool_calls` errors

Check:

- the final message type;
- whether the selected model supports Tool Calling;
- whether tools were actually bound;
- whether provider compatibility matches LangChain expectations.

An “OpenAI-compatible” provider may not implement all Tool Calling details identically.

---

# 36. SSE response is not `text/event-stream`

Chat should use:

```python
StreamingHttpResponse(..., content_type='text/event-stream')
```

If it becomes a normal DRF `Response`, the frontend streaming client will reject the content type or wait for a non-streaming body.

---

# 37. SSE streams on the server, but browser receives everything at once

Common cause: proxy buffering.

The backend sets headers such as:

```text
X-Accel-Buffering: no
Cache-Control: no-cache
```

A production reverse proxy may still need explicit SSE buffering configuration.

Test through the actual deployed path, not only Django `runserver`.

---

# 38. SSE text appears, but chat history disappears after reload

Check whether normal completion reached message persistence.

Inspect Django Admin / database for `Message` rows.

If no row exists, determine whether:

```text
stream was cancelled
worker raised an exception
generator disconnected before normal completion
persistence failed
```

Current cancellation semantics do not treat every partial stream as a completed persisted Message.

---

# 39. Clicking Stop hides output, but request keeps running

Current frontend should use a real `AbortController`.

Trace:

```text
InputField.vue
  ↓ signal
streamApi.js
  ↓
network request closes
```

If you only increment a `processId`, stale callbacks may be ignored while the underlying request/model continues.

---

# 40. Stop closes Network, but backend worker keeps running

Trace the server cleanup path:

```text
StreamingHttpResponse generator closes
  ↓
finally
  ↓
cancel_event.set()
  ↓
worker checks cancellation
```

Also remember that remote provider cancellation can be best-effort depending on the API/provider.

---

# 41. Long-term memory stays empty

Check:

```text
Message count reached the update trigger?
SystemPrompt title='记忆' exists?
Memory model/provider available?
update_memory() executed?
```

The learning implementation uses a simple periodic trigger based on Message count.

---

# 42. Long-term memory is updated but not used in chat

You persisted `Friend.memory` but may not be adding it back into the normal SystemMessage/context.

Trace:

```text
Friend.memory
  ↓
add_system_prompt / context assembly
  ↓
LLM messages
```

---

# 43. Memory starts inventing facts

This is often a prompt/model/data-quality problem, not a relational database bug.

A safer memory prompt should instruct the model to:

```text
keep stable useful facts
avoid inference not stated by user
avoid treating one-off emotion as permanent
prefer newer explicit facts when conflicts exist
keep output bounded
```

For higher assurance, move toward structured memory with provenance and evaluation.

---

# 44. ASR endpoint returns 503

Check:

```env
ENABLE_ASR=true
```

then:

```bash
python manage.py doctor
```

A disabled feature returning 503 is intentional and preferable to an obscure missing-WSS exception.

---

# 45. ASR WebSocket connection fails

Check:

```text
WSS_URL
API_KEY
ASR_MODEL
DNS/TLS
provider account permission
WebSocket payload protocol
```

ASR is a separate WebSocket integration, not the same connection as the chat HTTP API.

---

# 46. ASR returns empty/wrong text

Inspect:

```text
actual audio encoding
PCM conversion
sample rate (e.g. 16 kHz as expected by current integration)
channel layout
provider partial/final events
sentence-end logic
```

Renaming a WebM/MP3 file to `.pcm` does not make it raw PCM.

---

# 47. Browser microphone/VAD does not work

First prepare static assets:

```bash
cd frontend
npm run setup:vad
```

Check:

```text
microphone permission
input device
public VAD files
ONNX Runtime files
browser console
```

Then run `doctor` if ASR itself is enabled.

---

# 48. Text works, TTS produces no audio

Check one boundary at a time:

```text
ENABLE_TTS=true?
Character has valid Voice?
TTS task started?
TTS receiver got bytes?
SSE contains audio field?
frontend Base64 decode works?
MediaSource supports audio/mpeg?
autoplay policy blocked play()?
```

Do not jump directly to the player code without verifying the backend received audio bytes.

---

# 49. Character has no Voice

Current text chat should not crash merely because speech is unavailable when TTS is disabled/not required.

For real TTS testing:

1. create/configure a valid Voice in Admin;
2. assign it to the Character;
3. enable TTS;
4. run `doctor`;
5. verify the provider-specific `voice_id`.

The `demo-voice` created for teaching is a placeholder and not automatically a valid provider voice.

---

# 50. Browser blocks audio autoplay

Modern browsers restrict autoplay without user interaction.

Try to keep playback causally connected to a user action such as Send/microphone interaction.

Inspect rejected `audio.play()` promises in Console.

---

# 51. `MediaSource.addSourceBuffer('audio/mpeg')` fails

Possible causes:

```text
browser does not support the MIME type
provider did not actually return MP3
streamed MP3 chunks are not appendable as expected
data was corrupted during Base64 encode/decode
```

Verify provider TTS format and inspect browser support before changing unrelated SSE code.

---

# 52. Audio stutters

Inspect:

```text
provider/network latency
audioQueue starvation
SourceBuffer errors
chunk sizes
LLM text chunks too fragmented for TTS
frequent MediaSource reset
```

A production optimization can batch text by punctuation/sentence length instead of forwarding every tiny content chunk directly to TTS.

---

# 53. `websockets.connect` API errors

The Python WebSockets library has breaking changes across major versions.

AiFriends pins dependency versions in `requirements.txt`.

For first reproduction:

```bash
pip install -r requirements.txt
```

Do not begin by upgrading every dependency; otherwise you are debugging framework-upgrade compatibility instead of the project.

---

# 54. Why not upgrade all dependencies immediately?

Because the tutorial/runtime is tested against specific versions.

Better sequence:

```text
reproduce with pinned versions
  ↓
upgrade one dependency
  ↓
run tests/build/CI
  ↓
fix/document compatibility
```

Current frontend install may report dependency vulnerabilities. Treat them as a targeted supply-chain audit task rather than blindly running a breaking `npm audit fix` without review.

---

# 55. Directly refreshing `/friend` returns server 404

Vue uses history-style routing.

A browser refresh for:

```text
/friend
```

hits the server first.

AiFriends includes a Django fallback for the SPA during the learning setup. Production Nginx/reverse-proxy deployment needs a corresponding SPA fallback.

---

# 56. Vite build succeeds, but Django references an old hashed JS file

Current project uses a Vite manifest:

```text
frontend build
  ↓
.vite/manifest.json
  ↓
backend/web/views/vite.py
  ↓
Django template uses real generated JS/CSS entry
```

If you reintroduce hard-coded asset hashes, the next build may break the page.

Run:

```bash
cd frontend
npm run build
```

and inspect the manifest/runtime template path.

---

# 57. Frontend build warns about a large entry bundle

A warning is not the same as a build failure.

The current project has identified initial-bundle size as a performance improvement area.

Potential work:

```text
route-level lazy loading
dynamic import
keep speech/VAD code out of initial bundle
bundle-size budget in CI
```

Measure before/after instead of hiding the warning threshold.

---

# 58. Docker learning image builds, but should I deploy it directly to production?

No. It is explicitly a learning/reproducibility image.

Production still needs deliberate choices for:

```text
WSGI/ASGI server
TLS / reverse proxy
PostgreSQL
persistent media/object storage
secret management
backups
rate limiting
metrics/tracing
process supervision
```

“Dockerized” does not automatically mean “production-ready.”

---

# 59. `/api/health/` fails

Call:

```bash
curl http://127.0.0.1:8000/api/health/
```

Check:

```text
status
database
ai_mode
feature flags
request_id
HTTP status
```

The health endpoint intentionally avoids secrets/private data.

If database status is degraded, solve the DB problem before debugging the model layer.

---

# 60. Need to correlate one failure across layers

Send your own request ID:

```http
X-Request-ID: debug-123
```

The middleware preserves/returns it.

Use the same ID in structured logs across:

```text
HTTP
chat worker
RAG
TTS
errors
```

Correlation is better than dumping entire prompts into logs.

---

# 61. How do I decide whether the problem is frontend or backend?

Use Network.

## No request sent

Likely frontend event/state/router logic.

## Request sent, returns 4xx/5xx

Inspect request data/auth/backend.

## Backend returns correct payload, UI does not change

Likely Vue state/component handling.

## SSE Network contains events, UI stays static

Inspect:

```text
streamApi onmessage
component event handling
history/reactive array updates
stale processId checks
```

---

# 62. Minimize the problem

If full chat is broken, rebuild the path in layers:

```text
1. Django fixed JSON
2. Django fixed SSE
3. frontend displays fixed SSE
4. mock chat end-to-end
5. real LLM non-speech text
6. LangGraph without Tools
7. add get_time Tool
8. add RAG Tool
9. add ASR
10. add TTS
```

Every successful step removes uncertainty.

This is **reducing variables**, not “giving up on the full system.”

---

# 63. Useful diagnostic information when opening an Issue

Do not only write:

```text
“It doesn't work.”
```

Provide:

```text
OS:
Python version:
Node version:
AI_MODE:
feature flags:
command you ran:
browser URL:
HTTP status:
request ID:
Django traceback:
frontend Console:
Network request/response:
files/config you changed:
```

Redact:

```text
API keys
JWTs
refresh tokens
private conversations
private documents
```

---

# 64. Reusable troubleshooting template

```text
[Goal]
What am I trying to do?

[Expected]
What should happen?

[Actual]
What happened instead?

[Mode]
AI_MODE:
ENABLE_RAG:
ENABLE_ASR:
ENABLE_TTS:

[Frontend]
Console:
Network URL/status/payload/event stream:

[Backend]
Traceback/log:
request_id:

[Environment]
OS:
Python:
Node:

[What I already tried]
...
```

This dramatically improves the quality of bug reports and maintainer triage.

---

# 65. Final rule: change one layer at a time

The hardest debugging situation is:

```text
change frontend
change backend
change model provider
upgrade dependencies
change database
change Docker config
```

all at once.

Prefer:

```text
reproduce
  ↓
identify layer
  ↓
one minimal change
  ↓
test
  ↓
commit
```

That is the transition from random trial-and-error to engineering debugging.
