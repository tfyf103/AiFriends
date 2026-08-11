# AiFriends System Architecture and Request Flow

🌐 **Language:** [简体中文](./ARCHITECTURE.md) | **English**

> This guide explains AiFriends by following **how data moves through the system**, not by describing frameworks in isolation.

For first-time setup, read [QUICK_START_EN.md](./QUICK_START_EN.md) first.

---

# 1. System overview

```text
┌──────────────────────────────────────────────────────────────┐
│                          Browser                             │
│                                                              │
│ Vue 3 / Router / Pinia / Axios / fetch-event-source         │
│ Character UI / Chat / Microphone / Audio playback           │
└───────────────────────────┬──────────────────────────────────┘
                            │
                       HTTP / SSE
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    Django + DRF Backend                      │
│                                                              │
│ Auth / Character / Friend / Message / Chat / ASR            │
│ Serializers / ORM / StreamingHttpResponse / Request IDs      │
└───────┬──────────────────────┬───────────────────────┬───────┘
        │                      │                       │
        ▼                      ▼                       ▼
┌──────────────┐      ┌──────────────────┐    ┌─────────────────┐
│   SQLite     │      │ LangGraph        │    │ Speech service  │
│              │      │ Agent + Memory   │    │ WebSocket       │
│ User         │      └────────┬─────────┘    │ ASR / TTS       │
│ Character    │               │              └─────────────────┘
│ Friend       │               ▼
│ Message      │      ┌──────────────────┐
│ Prompt/Voice │      │ LLM / Embedding  │
└──────────────┘      └────────┬─────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │ LanceDB          │
                      │ Vector storage   │
                      └──────────────────┘
```

The project intentionally supports three runtime modes:

```text
mock  → no external AI provider required
text  → real chat model, optional RAG/speech
full  → Chat + RAG + ASR + TTS
```

This separation is important for reproducibility: learners can first understand the web and streaming architecture before adding external model/provider complexity.

---

# 2. Repository map

Read the repository by responsibility rather than opening files alphabetically.

```text
AiFriends/
├── backend/
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py
│   │   └── urls.py
│   └── web/
│       ├── ai/                  # runtime modes / feature flags
│       ├── models/              # relational data model
│       ├── serializers/         # DRF validation for migrated endpoints
│       ├── views/               # APIs and chat runtime
│       ├── documents/           # RAG / embeddings / LanceDB
│       ├── management/commands/ # doctor / seed_demo
│       ├── middleware.py        # X-Request-ID
│       └── tests.py
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── scripts/                 # VAD setup / quality checks
│   ├── tests/
│   └── src/
│       ├── main.js
│       ├── router/
│       ├── stores/
│       ├── js/http/             # Axios / refresh / SSE
│       ├── views/
│       └── components/
│
├── docs/
├── labs/
├── scripts/                     # course grader / RAG eval
├── evals/
└── .github/workflows/ci.yml
```

---

# 3. Three mental models

## Frontend

```text
View
  ↓
Component
  ↓
Pinia / Router
  ↓
HTTP client / SSE client
```

## Backend

```text
URL
  ↓
APIView / Serializer
  ↓
ORM / AI service
  ↓
Database / external provider
```

## AI workflow

```text
Messages
  ↓
LangGraph
  ↓
LLM
  ↓
Tool call?
  ├─ no  → answer
  └─ yes → ToolNode → LLM → answer
```

The important engineering lesson is that these layers are connected but should still be debugged independently.

---

# 4. Frontend boot path

```text
frontend/index.html
      ↓
frontend/src/main.js
      ↓
createApp(App)
      ↓
Pinia + Router
      ↓
App.vue
      ↓
RouterView
      ↓
page component
```

`main.js` is the browser application entry point.

In development, Vite also proxies:

```text
/api   → Django
/media → Django
```

This keeps browser requests same-origin from the learner’s point of view and reduces local CORS/cookie-host friction.

---

# 5. Authentication flow

A simplified login flow:

```text
username + password
        ↓
Login API
        ↓
DRF validation / credential check
        ↓
access token + refresh cookie
        ↓
Pinia stores access token
        ↓
Axios request interceptor
        ↓
Authorization: Bearer <access>
        ↓
Django / DRF authentication
        ↓
request.user
```

The refresh cookie is HttpOnly. Development cookie security is centralized so local HTTP does not accidentally require a production-only Secure cookie.

## Access-token refresh

Both normal Axios requests and SSE use the same refresh operation.

```text
request returns 401
      ↓
refreshAccessToken()
      ↓
single-flight guard
      ↓
one refresh request for concurrent callers
      ↓
Pinia receives new access token
      ↓
failed request reconnects/retries with new token
```

The shared single-flight mechanism prevents a burst of simultaneous expired requests from creating a refresh storm.

---

# 6. DRF validation and status codes

Authentication endpoints are the project’s reference implementation for moving from ad-hoc request parsing toward explicit DRF validation.

Examples:

```text
invalid request data      → 400
invalid login credentials → 401
username conflict         → 409
registration success      → 201
```

Machine-readable error codes are introduced alongside human-readable messages so the frontend does not have to infer behavior from text alone.

---

# 7. Core relational model

Simplified relationship model:

```text
Django User
    │
    │ 1:1
    ▼
UserProfile
    │
    ├──────────────► Character ─────► Voice
    │
    └──────────────► Friend ◄─────── Character
                         │
                         ├──────────► Message
                         │
                         └── memory

SystemPrompt is stored separately as operational prompt configuration.
```

## Why `Friend` exists

`Character` describes the reusable role:

```text
name
avatar
background
profile / persona
voice
creator
```

`Friend` describes one user’s relationship with that character:

```text
me
character
memory
create_time
update_time
```

Therefore:

```text
Character = role definition
Friend    = user-specific relationship/context
```

Long-term memory belongs on `Friend` because two users talking to the same Character should not share the same personal memory.

The database also enforces one Friend per `(user, character)` pair with a `UniqueConstraint`. The migration that introduced this constraint first consolidates possible legacy duplicates and moves Message history before enforcing uniqueness.

---

# 8. Normal JSON request flow

A normal API request looks like:

```text
Vue component
   ↓ api.post()/get()
Axios
   ↓ Authorization
HTTP
   ↓
Django URL
   ↓
APIView
   ↓
Serializer / ORM
   ↓
Response(JSON)
   ↓
Promise
   ↓
Vue updates state
```

Chat is different because the answer is generated incrementally.

---

# 9. Why chat uses SSE

A non-streaming LLM request creates a poor interaction pattern:

```text
user sends request
      ↓
model generates for several seconds
      ↓
user sees nothing
      ↓
complete response arrives
```

AiFriends uses:

```text
StreamingHttpResponse + Server-Sent Events
```

so model output can be delivered in chunks.

---

# 10. Frontend chat path

The main input component is:

```text
frontend/src/components/character/chat_field/input_field/InputField.vue
```

On send:

```text
handleSend()
   ↓
validate / trim input
   ↓
append user message optimistically
   ↓
append empty AI message
   ↓
create AbortController
   ↓
streamApi()
   ↓
POST /api/friend/message/chat/
```

Why create an empty AI message first?

Because incoming chunks should progressively update one bubble:

```text
''
'H'
'He'
'Hello'
'Hello ...'
```

instead of creating one bubble per token/chunk.

---

# 11. `streamApi` responsibilities

The SSE wrapper owns protocol details so UI components do not duplicate them.

Its responsibilities include:

```text
1. build Authorization header
2. POST JSON
3. validate the event-stream response
4. parse SSE events
5. handle [DONE]
6. refresh an expired access token
7. reconnect with the new token
8. propagate AbortSignal cancellation
9. surface protocol/network errors
```

This is an important separation:

```text
InputField = chat UX/state
streamApi  = transport/auth/retry details
```

---

# 12. Real cancellation

AiFriends uses two layers of cancellation.

## Browser

`AbortController` aborts the actual fetch/SSE request.

```text
user clicks Stop
      ↓
AbortController.abort()
      ↓
network stream closes
      ↓
UI stops accepting new output
      ↓
audio playback is stopped/cleaned
```

A process/stale-response identifier remains useful as extra UI protection against callbacks from an obsolete conversation.

## Backend

The Django streaming generator owns a `threading.Event` cancellation signal.

```text
client disconnects / generator closes
      ↓
finally sets cancellation event
      ↓
worker checks cancellation
      ↓
stop generating/sending as soon as practical
```

This is more meaningful than only hiding old output in the UI.

---

# 13. Backend chat entry

At a high level:

```text
MessageChatView.post()
      ↓
read friend_id + message
      ↓
authentication / ownership
      ↓
build prompt and recent history
      ↓
inspect AI_MODE
      ├─ mock → deterministic local stream
      └─ text/full → CharGraph
                        ↓
                     LLM / tools
      ↓
StreamingHttpResponse
```

Mock mode still uses the real authenticated web/SSE/persistence path; it simply replaces external AI generation with deterministic local output.

---

# 14. Prompt composition

Conceptually, a real chat request builds:

```text
SystemMessage
├── operational reply prompt
├── Character.profile
└── Friend.memory

HumanMessage / AIMessage
└── recent persisted conversation history

HumanMessage
└── current user input
```

Resulting context resembles:

```text
System: system rules + persona + long-term memory
Human:  previous question
AI:     previous answer
Human:  previous question
AI:     previous answer
...
Human:  current question
```

This separation helps learners understand three different concepts:

```text
Character.profile = who the character is
recent Messages   = short-term conversation context
Friend.memory     = compressed long-term user-specific memory
```

---

# 15. LangGraph execution model

```text
             ┌───────────────┐
             │     START     │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │     agent     │
             │   LLM call    │
             └───────┬───────┘
                     │
                tool_calls?
                 /       \
               no         yes
               │           │
               ▼           ▼
             ┌─────┐   ┌──────────┐
             │ END │   │ ToolNode │
             └─────┘   └────┬─────┘
                             │
                             └────────► agent
```

The model decides whether it needs a tool, but `bind_tools()` alone does not execute arbitrary Python. `ToolNode` is part of the controlled execution graph that performs the tool call and places the result back into the message state.

A typical tool sequence is:

```text
HumanMessage
  ↓
AIMessage(tool_calls=[...])
  ↓
ToolMessage(result=...)
  ↓
AIMessage(final natural-language answer)
```

---

# 16. RAG retrieval flow

RAG is implemented as a tool available to the Agent when the feature is enabled.

Online query path:

```text
LLM decides external knowledge is needed
      ↓
search_knowledge_base(query)
      ↓
retrieval.search_documents(query, k)
      ↓
embed query
      ↓
LanceDB similarity search
      ↓
Top-k Documents
      ↓
content + safe source labels
      ↓
ToolMessage
      ↓
Agent calls LLM again
      ↓
final answer
```

Retrieval is intentionally separated from the Agent so it can be evaluated independently.

---

# 17. Knowledge-base indexing

Offline/indexing path:

```text
data.txt
   ↓ TextLoader
Document
   ↓ RecursiveCharacterTextSplitter
chunks
   ↓ custom embeddings
vectors
   ↓
LanceDB
```

Current teaching defaults use approximately:

```text
chunk_size    = 500
chunk_overlap = 50
```

The important lesson is not the LanceDB brand. The reusable RAG model is:

```text
Knowledge
  ↓ chunk
Chunks
  ↓ embed
Vectors
  ↓ retrieve
Relevant evidence
  ↓
LLM
```

---

# 18. RAG evaluation

AiFriends includes a retrieval-only evaluation path.

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

The evaluation separates:

```text
Did retrieval return the expected evidence/source?

from

Did the LLM use the evidence correctly?
```

This distinction prevents every bad final answer from being incorrectly blamed on generation.

Source labels are normalized so the RAG result does not expose an absolute server filesystem path.

---

# 19. Long-term memory

Persisted raw Messages remain the conversation record. `Friend.memory` is a compressed long-term summary.

Conceptual update path:

```text
conversation Messages
      ↓
periodic memory trigger
      ↓
operational memory prompt
+ previous Friend.memory
+ recent Messages
      ↓
MemoryGraph
      ↓
LLM summary
      ↓
Friend.memory
```

The MemoryGraph is intentionally simpler than the chat Agent graph:

```text
START → agent → END
```

That demonstrates that LangGraph is a workflow-modeling tool, not a requirement to create complex loops everywhere.

`Friend.memory` is currently free-form text; structured memory is an explicit future engineering topic rather than silently changing the existing data model in one migration.

---

# 20. Text-only vs TTS chat

Speech is optional.

```text
AI_MODE=text
ENABLE_TTS=false
```

can stream real LLM text without opening a TTS WebSocket.

When TTS is enabled and a valid voice is available, text and speech are bridged concurrently.

---

# 21. TTS concurrency model

A simplified view:

```text
Django SSE generator
        │
        ▼
      Queue
        ▲
        │
 background worker/thread
        │
   asyncio / WebSocket
      /             \
     /               \
LLM text sender    TTS receiver
     │                 │
text chunks          audio bytes
     │                 │
     └──────► Queue ◄──┘
                 │
                 ▼
                SSE
```

The queue bridges execution models:

```text
async model/WebSocket work
        ↕
thread-safe Queue
        ↕
synchronous Django streaming generator
```

---

# 22. Mixing text and audio in SSE

Text event:

```json
{"content": "hello"}
```

Audio event:

```json
{"audio": "BASE64..."}
```

The frontend branches by key:

```text
content → append to current AI bubble

audio   → Base64 decode → playback queue / MediaSource
```

Base64 is used because SSE is text-oriented while TTS produces binary audio bytes.

---

# 23. ASR direction

ASR and TTS solve opposite directions.

```text
ASR: user audio → text
TTS: AI text    → audio
```

The browser uses voice-activity detection before/around microphone capture, prepares PCM/audio input, and sends speech to the backend/provider path. The backend returns recognized text that can then be placed into the normal message workflow.

Before enabling voice locally:

```bash
cd frontend
npm run setup:vad
```

This prepares VAD model/worklet and ONNX Runtime assets reproducibly from npm dependencies.

---

# 24. Build integration

Vite produces a build manifest instead of forcing Django templates to hard-code hashed JavaScript filenames.

```text
Vite build
   ↓
.vite/manifest.json
   ↓
Django reads entry assets
   ↓
index.html renders current CSS/JS paths
```

This removes a common stale-hash failure after rebuilding the frontend.

---

# 25. Health and request correlation

Public health endpoint:

```text
GET /api/health/
```

It reports non-secret readiness information such as database status, selected AI mode, and feature states.

Request middleware also creates or preserves:

```text
X-Request-ID
```

This provides a correlation identifier for tracing one request through logs and responses.

---

# 26. Testing and CI architecture

The project uses multiple feedback layers.

```text
manage.py doctor
      ↓
environment readiness

scripts/grade.py
      ↓
course structural requirements

Django / Node tests
      ↓
behavioral regression protection

Vite build / Docker build
      ↓
build reproducibility

GitHub Actions
      ↓
clean-environment integration gate
```

Current CI validates:

```text
Python compile
Chapter 00–20 structural grader
Django migration drift
Django system checks
Backend tests
npm ci
VAD setup
Frontend quality check
Frontend unit tests
Vite production build
Learning Docker image build
```

A structural grader is not a replacement for behavior tests; behavior tests are not a replacement for browser E2E; and a learning Docker build is not a production deployment guarantee.

---

# 27. Learning Docker boundary

`Dockerfile.learning` and `compose.learning.yml` exist as reproducibility/teaching tools.

They intentionally do **not** claim to be production deployment templates.

Production topics still include:

```text
production WSGI/ASGI server
Nginx / HTTPS
PostgreSQL
persistent media/object storage
secret management
rate limiting
metrics / tracing
```

This explicit boundary is part of the course: “it runs in a container” is not the same as “it is production-ready.”

---

# 28. Full message lifecycle

Putting the major pieces together:

```text
User types in InputField.vue
        ↓
optimistic user + empty AI messages
        ↓
AbortController + streamApi
        ↓
Authorization: Bearer <access>
        ↓
Vite proxy / Django URL
        ↓
MessageChatView
        ↓
Friend ownership
        ↓
SystemPrompt
+ Character.profile
+ Friend.memory
+ recent Message history
        ↓
AI_MODE
 ├─ mock → deterministic local stream
 └─ text/full → CharGraph
                  ↓
                 LLM
                  ↓
               ToolNode?
               ├─ time
               └─ RAG retrieval
                    ↓
                evidence/source
        ↓
text chunks
   ├──────────────→ SSE content
   └→ optional TTS WebSocket
                       ↓
                    audio bytes
                       ↓
                    Base64
                       ↓
                    SSE audio
        ↓
Vue onmessage
   ├─ update AI bubble
   └─ audio playback
        ↓
Message persistence
        ↓
periodic long-term memory update
```

This is the core systems model learners should be able to explain by the end of Chapter 13.

---

# 29. Where to debug first

Use symptoms to choose a layer.

| Symptom | First layer to inspect |
|---|---|
| Send button creates no request | Vue event / `handleSend` |
| HTTP 401 | access token / refresh flow |
| SSE has content but UI is empty | `streamApi` → callback → reactive history |
| Normal chat works, knowledge answer is wrong | retrieval results before blaming LLM |
| Text works, audio does not | TTS WebSocket / audio event path |
| Old stream writes into new chat | cancellation / process ID / stale callback |
| User-specific memory missing | `Friend.memory` update + prompt composition |
| Build serves old hashed file | Vite manifest / Django asset lookup |

A useful debugging order is:

```text
UI
 ↓
Vue state
 ↓
Network
 ↓
JWT
 ↓
Django URL/View
 ↓
ORM / permissions
 ↓
AI mode/config
 ↓
LLM
 ↓
Tool / Retrieval
 ↓
SSE
 ↓
ASR/TTS
```

---

# 30. Known engineering boundaries

AiFriends is an active educational engineering project, not a finished production platform. Current areas intentionally left for future work include:

- broader Serializer/error-schema migration across legacy APIs;
- refresh-token blacklist/revocation integration;
- stronger file upload MIME/size/image validation;
- browser-level E2E coverage;
- structured long-term memory;
- first-class RAG citation events/UI;
- dependency/supply-chain hardening;
- route-level lazy loading and bundle budgets;
- production server/Nginx/PostgreSQL/persistent media/metrics.

These are not hidden shortcomings; they are part of the engineering curriculum and roadmap.

---

# 31. Recommended source-reading order

## Frontend

```text
frontend/src/main.js
  ↓
frontend/src/router/
  ↓
frontend/src/stores/
  ↓
frontend/src/js/http/api.js
  ↓
frontend/src/js/http/authRefresh.js
  ↓
frontend/src/js/http/streamApi.js
  ↓
InputField.vue
  ↓
Microphone.vue
```

## Backend

```text
backend/web/urls.py
  ↓
backend/web/models/
  ↓
backend/web/serializers/account.py
  ↓
backend/web/views/friend/message/chat/chat.py
  ↓
backend/web/views/friend/message/chat/graph.py
  ↓
backend/web/views/friend/message/memory/
  ↓
backend/web/documents/retrieval.py
  ↓
backend/web/views/friend/message/asr/
```

## Engineering infrastructure

```text
backend/web/ai/config.py
backend/web/management/commands/doctor.py
backend/web/management/commands/seed_demo.py
backend/web/middleware.py
backend/web/views/health.py
backend/web/tests.py
scripts/grade.py
scripts/eval_rag.py
.github/workflows/ci.yml
Dockerfile.learning
```

---

# 32. Continue learning

Recommended English labs:

- [Chapter 00 — Environment](../labs/en/chapter-00-environment.md)
- [Chapter 06 — Minimal LLM Chat](../labs/en/chapter-06-basic-chat.md)
- [Chapter 07 — SSE Streaming](../labs/en/chapter-07-sse.md)
- [Chapter 08 — LangGraph Tool Calling](../labs/en/chapter-08-langgraph-tools.md)
- [Chapter 10 — RAG + LanceDB](../labs/en/chapter-10-rag.md)
- [Chapter 13 — Full-System Capstone](../labs/en/chapter-13-capstone.md)

Return to the [English Learning Hub](./README_EN.md).
