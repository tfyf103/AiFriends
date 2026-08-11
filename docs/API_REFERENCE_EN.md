# AiFriends API Reference

🌐 **Language:** [简体中文](./API_REFERENCE.md) | **English**

> This document follows the current `backend/web/urls.py` and maintained Views.
>
> The goal is not to memorize URLs. You should be able to answer: **who sends the request, whether authentication is required, where the data goes, what success/error status means, and whether the response is JSON or SSE.**

---

# 1. Local Base URL and Vite Proxy

In development the browser normally talks to Vite:

```text
Browser http://localhost:5173
        ↓ /api/... /media/...
Vite proxy
        ↓
Django http://127.0.0.1:8000
```

Frontend code can therefore call:

```js
api.get('/api/health/')
```

instead of hard-coding the Django host in every component.

This also reduces local CORS/cookie-host friction.

When you call Django directly with curl/Postman, use:

```text
http://127.0.0.1:8000
```

---

# 2. Endpoint Overview

| Method | Path | Auth | Request | Response | Purpose |
|---|---|---|---|---|---|
| GET | `/api/health/` | No | - | JSON | Health / AI mode |
| POST | `/api/user/account/register/` | No | JSON | JSON + Cookie | Register |
| POST | `/api/user/account/login/` | No | JSON | JSON + Cookie | Login |
| POST | `/api/user/account/refresh_token/` | Refresh Cookie | empty | JSON + Cookie | Rotate refresh / issue access |
| POST | `/api/user/account/logout/` | Bearer | empty | JSON | Delete refresh cookie |
| GET | `/api/user/account/get_user_info/` | Bearer | - | JSON | Current user |
| POST | `/api/user/profile/update/` | Bearer | multipart | JSON | Update profile |
| POST | `/api/create/character/create/` | Bearer | multipart | JSON | Create Character |
| POST | `/api/create/character/update/` | Bearer | multipart | JSON | Update owned Character |
| POST | `/api/create/character/remove/` | Bearer | JSON | JSON | Remove owned Character |
| GET | `/api/create/character/get_single/` | Bearer | query | JSON | Read Character for editing |
| GET | `/api/create/character/get_list/` | depends on current View | query | JSON | Character list |
| GET | `/api/create/character/voice/get_list/` | Bearer | - | JSON | Voice list |
| GET | `/api/homepage/index/` | No | query | JSON | Homepage / search |
| POST | `/api/friend/get_or_create/` | Bearer | JSON | JSON | Create/read Friend |
| POST | `/api/friend/remove/` | Bearer | JSON | JSON | Remove Friend |
| GET | `/api/friend/get_list/` | Bearer | query | JSON | Friend list |
| POST | `/api/friend/message/chat/` | Bearer | JSON | **SSE** | AI Chat |
| GET | `/api/friend/message/get_history/` | Bearer | query | JSON | Message history |
| POST | `/api/friend/message/asr/asr/` | Bearer | multipart | JSON | PCM → text |

> Some older CRUD endpoints still use legacy response conventions. Authentication, Health, Chat validation, and newer engineering paths demonstrate more accurate status codes. Chapter 15 is the migration path toward more consistent Serializer/error contracts across the whole API.

---

# 3. HTTP Status Semantics

Current core paths already use status classes such as:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
404 Not Found
409 Conflict
503 Service Unavailable
```

Think of them as two layers:

```text
HTTP status
  → broad protocol/result category

JSON result/code/message/errors
  → application-specific meaning
```

Example:

```text
409 Conflict
code = USERNAME_EXISTS
```

The frontend should not need to parse a human-language sentence to know the class of failure.

---

# 4. JWT Authentication Model

## 4.1 Access Token

The frontend keeps the access token in application state (Pinia).

Normal protected HTTP requests and SSE requests send:

```http
Authorization: Bearer <access-token>
```

DRF authentication resolves this to:

```python
request.user
```

Business Views should use `request.user` for identity instead of trusting a client-provided user ID.

---

## 4.2 Refresh Token

The refresh token is stored in an HttpOnly Cookie.

Normal JavaScript does not directly read the token value; the browser sends the cookie to:

```text
POST /api/user/account/refresh_token/
```

Cookie behavior is centralized in:

```text
backend/web/views/user/account/cookies.py
```

Development and production differ intentionally:

```text
DEBUG=true / plain HTTP → Secure cookie disabled for local learning
DEBUG=false / HTTPS     → Secure cookie enabled
```

---

## 4.3 Shared Single-Flight Refresh

Current frontend refresh code is shared by normal Axios requests and SSE:

```text
frontend/src/js/http/authRefresh.js
frontend/src/js/utils/singleFlight.js
```

Concurrent expiration behaves like:

```text
A → 401 ─┐
B → 401 ─┼→ one refresh Promise
C → 401 ─┘        ↓
              new access → Pinia
                   ↓
                A/B/C retry
```

A historical SSE bug refreshed successfully but retried with stale access. The maintained path now rebuilds the stream request after updating Pinia.

---

# 5. Health API

```http
GET /api/health/
```

No authentication required.

Example in Mock mode:

```json
{
  "status": "ok",
  "database": "ok",
  "ai_mode": "mock",
  "features": {
    "rag": false,
    "asr": false,
    "tts": false
  },
  "request_id": "..."
}
```

The response also contains:

```http
X-Request-ID: ...
```

The endpoint intentionally does **not** expose:

```text
API keys
database passwords
private configuration
full stack traces
private conversation content
```

If the database check fails, the endpoint can return a degraded status with:

```text
HTTP 503 Service Unavailable
```

---

# 6. Register

```http
POST /api/user/account/register/
Content-Type: application/json
```

Body:

```json
{
  "username": "alice",
  "password": "secret123"
}
```

Success:

```text
HTTP 201 Created
```

Example response shape:

```json
{
  "result": "success",
  "access": "<jwt>",
  "user_id": 1,
  "username": "alice",
  "photo": "/media/...",
  "profile": "..."
}
```

A refresh HttpOnly Cookie is also set.

Common error classes:

```text
400 Bad Request → invalid/blank input
409 Conflict    → username already exists
```

Registration uses Django's:

```python
User.objects.create_user(...)
```

so the password is hashed rather than stored as plaintext.

---

# 7. Login

```http
POST /api/user/account/login/
Content-Type: application/json
```

Body:

```json
{
  "username": "alice",
  "password": "secret123"
}
```

Core authentication:

```python
user = authenticate(username=username, password=password)
```

Typical status behavior:

```text
200 OK            valid credentials
400 Bad Request   invalid input shape/blank values
401 Unauthorized  username/password do not authenticate
```

Success returns access JSON and sets the refresh cookie.

---

# 8. Refresh

```http
POST /api/user/account/refresh_token/
Cookie: refresh_token=...
```

Body may be empty:

```json
{}
```

Success:

```json
{
  "result": "success",
  "access": "<new access>"
}
```

The refresh cookie is rotated according to the current JWT/cookie configuration.

Missing/invalid/expired refresh credentials result in an authentication failure rather than a successful empty response.

---

# 9. Logout

```http
POST /api/user/account/logout/
Authorization: Bearer <access>
```

Success example:

```json
{
  "result": "success"
}
```

The backend removes the refresh cookie and the frontend clears its user/access state.

> Current project cleanup removes the cookie. Full refresh-token blacklist/revocation integration remains a separate hardening step.

---

# 10. Get Current User

```http
GET /api/user/account/get_user_info/
Authorization: Bearer <access>
```

Example:

```json
{
  "result": "success",
  "user_id": 1,
  "username": "alice",
  "photo": "/media/...",
  "profile": "..."
}
```

On a full browser refresh, Pinia memory is empty. The app can restore access through the refresh cookie, then load current user state again.

---

# 11. Profile Update

```http
POST /api/user/profile/update/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

Form fields include:

```text
username
profile
photo?  optional
```

This endpoint remains a useful Chapter 15 Serializer/error-contract refactoring target.

---

# 12. Character Create

```http
POST /api/create/character/create/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

Fields:

```text
name
voice_id
profile
photo
background_image
```

Data flow:

```text
Vue FormData
  ↓
request.data + request.FILES
  ↓
resolve authenticated UserProfile
  ↓
resolve Voice
  ↓
Character.objects.create(...)
  ↓
SQLite metadata + media files
```

`author` must be derived from authentication, not trusted from a browser-supplied owner ID.

---

# 13. Character Update

```http
POST /api/create/character/update/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

Typical fields:

```text
character_id
name
voice_id
profile
photo?             optional
background_image?  optional
```

The backend must re-check object ownership, conceptually:

```text
Character.author.user == request.user
```

This is **object-level authorization**.

---

# 14. Character Remove / Get Single / List / Voice

Remove:

```http
POST /api/create/character/remove/
Authorization: Bearer <access>
```

Read an owned Character for editing:

```http
GET /api/create/character/get_single/?character_id=...
Authorization: Bearer <access>
```

Voice list:

```http
GET /api/create/character/voice/get_list/
Authorization: Bearer <access>
```

When working on these endpoints, treat client IDs as untrusted selectors that still require server-side ownership/visibility policy.

---

# 15. Homepage / Search

```http
GET /api/homepage/index/?items_count=0&search_query=...
```

No authentication required for the public discovery feed.

Current pagination is offset-like:

```text
items_count : items_count + 20
```

Search matches Character name/profile using case-insensitive containment.

The frontend must reset the list/pagination when the search query changes.

---

# 16. Friend Get or Create

```http
POST /api/friend/get_or_create/
Authorization: Bearer <access>
Content-Type: application/json
```

Body:

```json
{
  "character_id": 12
}
```

Business meaning:

```text
current UserProfile × one Character
```

Friend also defines the boundary for:

```text
chat history
long-term memory
```

Current `main` uses `get_or_create()` and a database-level uniqueness constraint on:

```text
(me, character)
```

so concurrent requests cannot legitimately persist duplicate relationships.

Creation may return a different success status than returning an already-existing relationship; clients should treat both as successful resolution of the requested Friend.

---

# 17. Friend List / Remove

List:

```http
GET /api/friend/get_list/?items_count=0
Authorization: Bearer <access>
```

Remove:

```http
POST /api/friend/remove/
Authorization: Bearer <access>
```

Private Friend operations must enforce:

```text
friend.me.user == request.user
```

on the server.

---

# 18. Chat — The Core Streaming API

```http
POST /api/friend/message/chat/
Authorization: Bearer <access>
Content-Type: application/json
```

Body:

```json
{
  "friend_id": 3,
  "message": "Hello"
}
```

Typical validation outcomes:

```text
400 Bad Request → blank/invalid message
404 Not Found   → Friend not found / not accessible to current user
```

The success response is **not one JSON document**.

```http
Content-Type: text/event-stream
```

Event examples:

```text
data: {"content":"Hel"}

data: {"content":"lo"}

data: {"audio":"...base64..."}

data: {"error":"..."}

data: [DONE]

```

---

# 19. Chat Runtime Modes

## Mock

```env
AI_MODE=mock
```

No real `CharGraph`/external model is required for generation.

The request still exercises real application layers:

```text
JWT
Friend ownership
SystemPrompt/history assembly
StreamingHttpResponse
SSE parsing
Vue updates
Message persistence
```

This makes Mock suitable for onboarding and CI.

## Text

```env
AI_MODE=text
```

Real LLM + SSE, with speech/RAG optional by feature flags.

## Full

Enables the complete intended set of model/RAG/speech capabilities, subject to feature flags and provider configuration.

---

# 20. Chat SSE Token Refresh

When the access token is expired as the stream opens:

```text
SSE HTTP 401
  ↓
refreshAccessToken()
  ↓
new access written to Pinia
  ↓
old stream attempt rejects/exits
  ↓
start a new request
  ↓
rebuild Authorization header from fresh state
```

Do not assume an already-open/failed fetch can magically mutate its old headers.

---

# 21. Chat Cancellation

Frontend:

```text
AbortController
```

is passed into the streaming client.

Stop flow:

```text
controller.abort()
  ↓
SSE request closes
  ↓
Django generator cleanup/finally
  ↓
cancel_event.set()
  ↓
worker stops producing LLM/TTS chunks as early as possible
```

Remote provider compute cancellation may still be best-effort depending on provider behavior.

---

# 22. Chat Persistence

On normal completion, a `Message` stores fields such as:

```text
friend
user_message
input
output
input_tokens
output_tokens
total_tokens
```

Current code intentionally distinguishes normal completion from cancelled streams.

A future design may add:

```text
partial
cancel_reason
status
```

to make cancelled/partial responses first-class history records.

---

# 23. Message History

```http
GET /api/friend/message/get_history/?friend_id=3&last_message_id=0
Authorization: Bearer <access>
```

Initial request:

```text
last_message_id=0
```

Older-page request:

```text
pk < last_message_id
```

The backend scopes history by the authenticated user so another user's Friend history cannot be read by changing the ID.

---

# 24. ASR

```http
POST /api/friend/message/asr/asr/
Authorization: Bearer <access>
Content-Type: multipart/form-data
```

Field:

```text
audio = PCM file
```

When:

```env
ENABLE_ASR=false
```

the endpoint returns a clear service-unavailable response instead of trying to open a missing provider WebSocket.

This is intentional feature isolation: text learning should not fail because the learner has no speech account.

---

# 25. Why TTS Has No Separate Browser HTTP Endpoint

TTS is part of the chat worker's optional parallel pipeline:

```text
LLM chunk
  ├→ Queue → SSE content
  └→ TTS WebSocket
       ↓
     MP3 bytes
       ↓ Base64
     Queue → SSE audio
```

When:

```env
ENABLE_TTS=false
```

chat uses the text path and does not connect to the speech WebSocket.

A Character without a usable Voice can also fall back to text-only behavior when TTS is not required.

---

# 26. RAG Is an Agent Tool, Not a Direct Browser Endpoint

Current RAG retrieval is wrapped for LangGraph Tool use.

Conceptually:

```text
search_knowledge_base(query)
  ↓
backend/web/documents/retrieval.py
  ↓
LanceDB similarity search
  ↓
source-aware evidence
```

The tool is only registered when:

```env
ENABLE_RAG=true
```

This keeps text-only mode independent from LanceDB setup.

---

# 27. RAG Source Safety and Evaluation

`document_source()` normalizes evidence source labels so absolute server paths are not exposed.

Retrieval can be evaluated separately with:

```bash
python scripts/eval_rag.py \
  --cases evals/rag_cases.example.json \
  --k 3
```

This distinguishes:

```text
retrieval failed
vs
evidence was retrieved but generation used it poorly
```

---

# 28. Request IDs

Middleware:

```text
backend/web/middleware.py
```

Clients may send:

```http
X-Request-ID: my-debug-id
```

Otherwise the server generates one.

The response includes the same/effective ID:

```http
X-Request-ID: ...
```

Future structured logs can correlate:

```text
HTTP
LLM
RAG
TTS
errors
```

with one request identifier.

---

# 29. Learn the API with curl

Health:

```bash
curl http://127.0.0.1:8000/api/health/
```

Register:

```bash
curl -i \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' \
  http://127.0.0.1:8000/api/user/account/register/
```

On Windows PowerShell, `Invoke-RestMethod` can be easier than debugging shell quoting differences.

---

# 30. Learn the API with DevTools

For each request inspect:

```text
Request URL
Method
Status
Request Headers
Payload / Form Data
Response Headers
Response / EventStream
```

For cookie/authentication debugging also inspect:

```text
Application → Cookies
```

---

# 31. Layered Error Diagnosis

## No Network request

Likely frontend event/state/router issue.

## 400

Input validation/request body.

## 401

Access/refresh/authentication flow.

## 403

Explicit permission denial where an endpoint uses it.

## 404

Wrong URL or hidden/not-found object/ownership resolution.

## 409

Business conflict such as duplicate username.

## 500

Start with the Django traceback/logs.

## 503

Required capability/service is unavailable, for example disabled ASR or degraded health.

## SSE returns 200 but no chunks

Trace:

```text
AI_MODE
worker
model
Queue
optional TTS
SSE generator
```

---

# 32. Source Index

Routing:

```text
backend/web/urls.py
```

Authentication:

```text
backend/web/views/user/account/
backend/web/serializers/account.py
frontend/src/js/http/api.js
frontend/src/js/http/authRefresh.js
frontend/src/js/http/streamApi.js
frontend/src/js/utils/singleFlight.js
```

Chat:

```text
backend/web/views/friend/message/chat/chat.py
backend/web/views/friend/message/chat/graph.py
```

AI config:

```text
backend/web/ai/config.py
```

Memory:

```text
backend/web/views/friend/message/memory/
```

RAG:

```text
backend/web/documents/retrieval.py
backend/web/documents/utils/
scripts/eval_rag.py
```

Health / request IDs:

```text
backend/web/views/health.py
backend/web/middleware.py
```

Frontend chat/voice:

```text
frontend/src/components/character/chat_field/input_field/InputField.vue
frontend/src/components/character/chat_field/input_field/Microphone.vue
```

---

# 33. Next API Engineering Steps

This document is a manually maintained teaching reference.

The next engineering layer can add:

```text
more Serializers
unified error envelope
error-code catalog
OpenAPI schema
Swagger UI
request/response examples generated from schema
browser E2E contracts
```

Machine-readable schema and teaching documentation are complementary:

```text
OpenAPI → precision/tooling
Teaching docs → architecture, debugging, and why the contract exists
```
