# Rebuild AiFriends from Scratch: Learn Full-Stack AI Through Real Git History

[简体中文](./COURSE_REBUILD.md) | **English**

> This course does not ask you to start by reading the final version of the codebase.
>
> It uses AiFriends' real Git history to reconstruct the project in the order it naturally evolved: **Vue pages → Django → JWT → Character CRUD → Friend relationships → basic chat → SSE → LangGraph → long-term memory → RAG → ASR → TTS**.
>
> The goal is not merely to understand this repository. The goal is to reach the point where **you can rebuild an AiFriends-like system in an empty directory and explain why each layer exists**.

> **Historical checkpoint note:** the commit SHAs in this guide are learning artifacts from the original project evolution. The current `main` branch has additional engineering work such as `AI_MODE=mock`, feature flags, serializers, cancellation, data constraints, safer RAG retrieval, health/request IDs, tests, and CI. Use historical commits to understand *why a capability appeared*; use the maintained docs and Labs for the current recommended implementation.

---

# 0. Why learn from real versions?

The maintained application contains many technologies at once:

```text
Vue 3
Vue Router
Pinia
Axios
JWT
Django
DRF
SQLite
SSE
LangChain
LangGraph
Tool Calling
Long-term Memory
Embedding
LanceDB
RAG
ASR
TTS
WebSocket
MediaSource
```

If a beginner opens the final chat implementation first, they can encounter all of this in one place:

```text
Django
threads
asyncio
Queue
LangGraph
LLM streaming
WebSocket
TTS
SSE
database persistence
```

That is a poor learning order.

Real products are not written in one day either. AiFriends' history exposes a more understandable progression:

```text
pages first
  ↓
backend + database
  ↓
user identity
  ↓
Character and Friend domain model
  ↓
LLM chat
  ↓
waiting feels too slow → SSE
  ↓
model capabilities are limited → Tool Calling
  ↓
history grows too long → Long-term Memory
  ↓
model lacks private/project knowledge → RAG
  ↓
voice input/output → ASR / TTS
```

This course therefore treats **real commits as chapter checkpoints**.

---

# 1. How to use Git history

## 1.1 Inspect one historical change

```bash
git show <commit-sha>
```

Example: inspect the first backend streaming implementation:

```bash
git show b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

Start with the file summary:

```bash
git show --stat b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

Ask:

- What user problem did this commit solve?
- Which layers changed?
- Where does data enter and where does it leave?
- What would stop working if the new code were removed?

## 1.2 Compare two stages

```bash
git diff <older-commit> <newer-commit>
```

For example, compare ordinary chat with the first streaming chat:

```bash
git diff 72a9866e3370481a8fa6e070e55c7784977c058a b9ea1c3404b04413d638067de78c3ed4d7262fc3
```

The useful question is not “what is SSE?” but:

> What exactly had to change to turn a blocking chat request into a streaming experience?

## 1.3 Temporarily inspect an old version

```bash
git switch --detach <commit-sha>
```

Example:

```bash
git switch --detach 72a9866e3370481a8fa6e070e55c7784977c058a
```

A detached HEAD is normal when you are only studying a snapshot.

## 1.4 Build from an old checkpoint

Do not develop permanently on detached HEAD. Create a learning branch:

```bash
git switch -c learn/chapter-06 72a9866e3370481a8fa6e070e55c7784977c058a
```

Return to the maintained project with:

```bash
git switch main
```

---

# 2. Prefer your own learning repository

If your goal is real mastery, create a separate directory or repository such as:

```text
AiFriends-Learning/
├── backend/
└── frontend/
```

Commit each small capability:

```bash
git add .
git commit -m "learn: chapter 01 vue router"
```

The original AiFriends commits become your **reference answers**. Your commits become your **learning trace**.

---

# 3. Course map

| Chapter | Topic | Core technologies | Outcome |
|---|---|---|---|
| 00 | Environment and skeleton | Git / Python / Node | Start the frontend/backend toolchains |
| 01 | Vue pages and routing | Vue / Router | Understand components and SPA navigation |
| 02 | Django and database | Django / ORM / SQLite | Understand URL → View → Model |
| 03 | Registration and login | REST / JWT / Pinia / Axios | Build the identity path |
| 04 | Character CRUD | CRUD / FormData / ImageField | Build a complete full-stack business flow |
| 05 | Homepage and Friend | ORM relations / API | Understand the relationship model |
| 06 | Basic AI Chat | LangChain / Messages | Complete one LLM conversation |
| 07 | SSE Streaming | StreamingHttpResponse / SSE | Stream incremental replies |
| 08 | Agent and Tools | LangGraph / ToolNode | Let the model choose and call tools |
| 09 | Long-term Memory | Summarization / Prompt | Compress history into durable memory |
| 10 | RAG | Chunk / Embedding / LanceDB | Build a retrievable knowledge base |
| 11 | ASR | PCM / WebSocket | Convert speech to text |
| 12 | TTS | asyncio / Queue / MediaSource | Speak while text is still being generated |
| 13 | Full Pipeline | Full-stack AI | Trace the complete system independently |

For the maintained exercise versions of these chapters, use [English Labs 00–20](../labs/en/README.md).

---

# Chapter 00 — Environment and project skeleton

## Real checkpoint

```text
cd5cfb2b387f4fb727cd55f33db36ac3a2a847f7  Initial local-project upload
```

## Learn first

```text
Git      = version control
Python   = Django backend runtime
Node.js  = Vue/Vite toolchain runtime
Browser  = frontend JavaScript runtime
```

Install Git, Python, Node.js, and an editor. Confirm:

```bash
git --version
python --version
node --version
npm --version
```

Do **not** start with LangChain, LangGraph, RAG, vector databases, or speech.

### Acceptance

You can explain why Vue and Django development normally uses separate processes/terminals.

---

# Chapter 01 — Vue pages, components, and routing

## Real checkpoints

```text
e03219b7464ea487f843f7abe74daa98eb7dfd7c  Create navigation bar
b1703e8eff39f95dcd8cf3ed7b5d1def0e616758  Implement routes
b938159da24699eaec1249251b99ec06884f6b0a  Implement login/register pages
```

## Minimal Vue mental model

```text
main.js
  ↓
createApp(App)
  ↓
App.vue
  ↓
View
  ↓
Component
```

## Router mental model

```text
URL
 ↓
Vue Router
 ↓
route match
 ↓
render the corresponding View
```

Build only these routes first:

```text
/
/user/account/login
/user/account/register
```

Learn `<script setup>`, `<template>`, scoped styles, `ref()`, `computed()`, props, and emits.

### Acceptance

Changing the URL changes the rendered view without a traditional full-page reload, and you can explain the difference between a View and a reusable Component.

---

# Chapter 02 — Django, ORM, and SQLite

## Real checkpoints

```text
3ab2bd28ca6551e188084e7502de82a06df96b0a  Complete the database layer
248a7d8ea7c24e32d6f6a5d3631e277e7a09bb87  Implement backend
```

## Four-layer mental model

```text
URL
 ↓
View
 ↓
Model / ORM
 ↓
Database
```

Create a Django project/app and learn:

```bash
django-admin startproject backend
python manage.py startapp web
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Migration model:

```text
models.py
   ↓ makemigrations
migration files
   ↓ migrate
database schema
```

### Acceptance

You can use Django Admin and explain why Admin is an interface over the database rather than “the database itself.”

---

# Chapter 03 — Registration, login, JWT, and global user state

## Real checkpoints

```text
a27cbf8f90cf256ab075173f19d468319b302f67  Connect frontend register/login/logout APIs
b0aa1d5c169d836023fd3788152d5cb1eb4bf55b  Restore user state after initial page load/refresh
e2915586d6352180b93500ce8e15dbfa8afa8704  Add profile-update API
8d06c1ec8c04a70a8a47a1644fd8cd28a63a48e6  Add profile-edit UI
```

## Identity flow

```text
Login form
  ↓ POST
Django login API
  ↓
access token + refresh token
  ↓
Pinia user state
  ↓
Axios Authorization header
```

The access token is short-lived and sent often. The refresh token lives longer and obtains a new access token.

Historical exercise targets:

```text
register
login
logout
refresh token
get user info
Pinia user store
Axios request/response handling
router guard
```

Use DevTools → Network and inspect:

```text
Authorization: Bearer <token>
```

### Current-main engineering note

The maintained code now centralizes refresh behavior and uses **single-flight refresh** so simultaneous requests do not create a refresh storm. Learn the original flow from history, then compare it with the maintained authentication path.

### Acceptance

Refreshing the browser restores authenticated user state instead of making the app “forget” the user.

---

# Chapter 04 — Character CRUD

## Real checkpoints

```text
2081304f049a58a404b39bfe09f9c373b80d24df  Character CRUD backend API
1c811b7034f042ed5344efe653e0a31e07c6e00a  CRUD backend fixes
84f1c92eba32c62ef2e5724a77eeb7c64979de6b  Character creation frontend
95cf0456ef46696bca36c602928fbbb6dbe658d5  Character update frontend
```

CRUD means Create, Read, Update, Delete.

The Character domain includes concepts such as:

```text
Character
├── author
├── name
├── photo
├── background_image
├── profile
└── voice
```

Images require you to learn:

```text
FormData
multipart/form-data
ImageField
MEDIA_ROOT
MEDIA_URL
```

### Acceptance

Trace one complete flow:

```text
Vue Form
 ↓
HTTP Request
 ↓
Django View
 ↓
Character Model
 ↓
SQLite + media/
 ↓
GET API
 ↓
Vue display
```

---

# Chapter 05 — Homepage, search, Friend relationships, chat shell

## Real checkpoints

```text
f96da725bbfd77aa9766f70786a6061f35f8dcb9  Homepage frontend/backend
c9ea5e0f3b1a276c3fe6d0b10fa648db3f5510ca  Search
102b31a0f60be51bbc6f22f690ec74d3ee0a5be3  Friend backend
fb1394362c3ba60bee544bf8737bca5051ea9ae8  Chat UI
1c9d9e000c77c4e1779e0681ae5fca7e8123dc67  Friend list frontend
```

## Relationship model

```text
UserProfile
    |
    | me
    v
Friend
    |
    | character
    v
Character
```

**Friend is not another human account.** It is the relationship between the current user and one AI Character.

Build homepage discovery, search, add/remove Friend, Friend list, and the chat shell.

Learn ORM traversal such as:

```python
Friend.objects.filter(me__user=request.user)
```

### Current-main engineering note

The maintained schema enforces a database-level uniqueness constraint for `(me, character)` and includes a safe migration for historical duplicates.

### Acceptance

Different logged-in users can only access their own Friend relationships.

---

# Chapter 06 — Start with the simplest AI chat

## Real checkpoints

```text
c82553f13badf75ba372f1bc343b0d14b0bc5081  Create Message database
72a9866e3370481a8fa6e070e55c7784977c058a  Implement chat backend
```

Do not add SSE, tools, memory, RAG, or TTS yet.

```text
user message
  ↓ POST
Django
  ↓
LLM
  ↓
complete text
  ↓ JSON
Vue
```

Learn only the LangChain concepts required by this need:

```text
HumanMessage
SystemMessage
AIMessage
ChatOpenAI
invoke()
```

Persist the conversation and token metadata in Message records.

### Acceptance

Chat works, but the UI remains empty until the model finishes. That discomfort creates the requirement for Chapter 07.

---

# Chapter 07 — SSE streaming chat

## Real checkpoints

```text
b9ea1c3404b04413d638067de78c3ed4d7262fc3  Backend text streaming
3c7c464b51dcbb411ad50bafe58ad214ecc6eb2c  Streaming frontend reply
031f03137cf8abb5128c3de93bc6f353b93965cf  Backend chat history
ea419695f4d8e9e2cec97c4f92a03dc7d679e4df  Streaming history loading
7ba85a3b629a9fdb41307fb6427960ffe674c2b9  Load 10 messages per batch
```

Blocking HTTP:

```text
Request → wait for complete result → Response
```

SSE:

```text
Request
  ↓
data chunk 1
  ↓
data chunk 2
  ↓
data chunk 3
  ↓
[DONE]
```

Backend concepts:

```python
StreamingHttpResponse
yield "data: ...\n\n"
```

Frontend concepts:

```text
fetchEventSource
onopen
onmessage
onerror
```

Maintained source paths:

```text
frontend/src/js/http/streamApi.js
frontend/src/components/character/chat_field/input_field/InputField.vue
backend/web/views/friend/message/chat/chat.py
```

### Current-main engineering note

The maintained frontend uses a real `AbortController`, the backend propagates cancellation with a `cancel_event`, and refresh-token handling is coordinated so SSE retries do not create parallel refresh storms.

### Acceptance

DevTools shows a long-lived request and the AI bubble grows incrementally.

---

# Chapter 08 — System Prompt, multi-turn context, LangGraph Tool Calling

## Real checkpoints

```text
3bcc4a8c8e169475af6c78b2ac19752b62625bdf  System prompt + multi-turn context
72c4c3ae5efb950e7b4f08cded3a37238e961c78  Function/tool call
```

Move from a plain model:

```text
messages → LLM → answer
```

to an Agent loop:

```text
messages
   ↓
agent / LLM
   ↓
Tool needed?
   ├─ No → END
   └─ Yes
       ↓
     ToolNode
       ↓
   Tool result
       ↓
     agent
       ↓
  final answer
```

Learn:

```text
StateGraph
AgentState
add_messages
Node
Edge
Conditional Edge
START / END
ToolNode
```

Three important layers:

1. `@tool` describes a Python function as a tool.
2. `llm.bind_tools(tools)` gives the model tool schemas; it does not execute functions.
3. `ToolNode(tools)` executes the selected tool calls.

Start with a time tool before adding RAG.

### Acceptance

A time question causes a tool call rather than the model guessing the current time.

---

# Chapter 09 — Long-term Memory

## Real checkpoint

```text
15a8a8427db9801f1fcc01da5d15cfdb97014111  Add long-term memory
```

Infinite raw chat history causes larger prompts, higher token cost, more latency, and eventually context-window pressure.

AiFriends introduced this pattern:

```text
recent Message history
       +
Friend.memory compressed summary
       ↓
current chat context
```

Memory update:

```text
old Friend.memory
       +
recent conversation
       ↓
MemoryGraph
       ↓
LLM summary
       ↓
new Friend.memory
```

Relevant maintained code:

```text
backend/web/views/friend/message/memory/graph.py
backend/web/views/friend/message/memory/update.py
backend/web/views/friend/message/chat/chat.py
```

### Experiment

Tell the Character several stable facts, continue chatting, inspect `Friend.memory`, then ask about one of the facts later.

### Acceptance

You can explain why “messages are stored in a database” and “the LLM has usable long-term memory” are different statements.

---

# Chapter 10 — RAG and LanceDB

## Real checkpoints

```text
57f4c78c35313360065169c8ff008c77bba914a4  Add knowledge base
4c099063991521cdb55e58171919d2b623110d77  Add vector-database creation
```

Understand RAG as two separate pipelines.

## A. Index/build

```text
source document
  ↓
Loader
  ↓
Document
  ↓
Text Splitter
  ↓
Chunks
  ↓
Embeddings
  ↓
Vectors
  ↓
LanceDB
```

## B. Query

```text
User question
  ↓
Embedding
  ↓
Query vector
  ↓
LanceDB similarity search
  ↓
Top documents
  ↓
Tool result
  ↓
LLM
```

Chunking improves retrieval granularity and keeps returned context manageable. Embeddings map text into vector space so retrieval is semantic rather than exact-string matching.

### Current-main engineering note

The maintained project extracts retrieval into `backend/web/documents/retrieval.py`, sanitizes source labels, and includes `scripts/eval_rag.py` so retrieval can be evaluated independently from generation.

### Acceptance

You can explain the responsibility of Loader, Splitter, Embedding, VectorStore, Retrieval, and LLM as separate layers.

---

# Chapter 11 — ASR: speech to text

## Real checkpoints

```text
02cbc4f7567ebbed95eba483724611c35b6f6b1f  Frontend voice input
5c0f6473fefad53542280257399d830663c8683a  Backend speech recognition
```

ASR means **Automatic Speech Recognition**:

```text
speech → text
```

Conceptual flow:

```text
Browser microphone
  ↓
PCM
  ↓ HTTP
ASRView
  ↓
WebSocket
  ↓
ASR provider
  ↓
transcription
  ↓
InputField.handleSend(text)
```

The important design principle is reuse:

```text
Keyboard ─┐
          ├─> handleSend() → the same Chat API
ASR text ─┘
```

### Current-main engineering note

ASR is feature-flagged and provider/model configuration is environment-driven. Historical provider/model choices are examples, not permanent requirements.

### Acceptance

Speech becomes correct text first, then that text travels through the same chat path as keyboard input.

---

# Chapter 12 — TTS: speak while generating

## Real checkpoints

```text
845dcb620d0ce2f77f50b8c8dc94b91de338a58b  Backend TTS
8615f6607406be373ae9ce7b09934d5a4da496c6  Frontend audio playback
88343a97f0d74570e10bfe3952c0192669876a61  Selectable voices
```

TTS means **Text To Speech**:

```text
text → speech
```

A high-latency design is:

```text
complete LLM text
  ↓
complete MP3 generation
  ↓
playback
```

AiFriends evolved toward a streaming design:

```text
LLM chunk
  ├─> SSE content → browser text
  └─> TTS WebSocket
          ↓
       MP3 bytes
          ↓ Base64
       Queue
          ↓
       SSE audio
          ↓
       Browser MediaSource
```

The concurrency bridge exists because the system combines synchronous Django streaming with asynchronous LangGraph and TTS work:

```text
Background Thread
  ↓
asyncio.run()
  ↓
async LLM + TTS tasks
  ↓
Queue
  ↓
synchronous event_stream()
  ↓
SSE
```

The browser receives audio chunks rather than a complete MP3 URL, so it uses a byte queue and MediaSource/SourceBuffer-style incremental playback.

### Acceptance

Audio can begin before the full text answer is finished.

---

# Chapter 13 — Capstone: trace the complete request

Given a user request such as:

```text
Please answer XXX using the knowledge base.
```

You should be able to answer, without guessing:

1. Which Vue component receives the input?
2. Which variable is bound by `v-model`?
3. What does `handleSend()` do?
4. Which API does `streamApi()` call?
5. Where does JWT enter the request?
6. Which Django URL rule matches?
7. Which APIView receives the request?
8. How is Friend ownership checked?
9. Where is `SystemPrompt` added?
10. Where is `Character.profile` added?
11. Where is `Friend.memory` added?
12. Where is recent Message history added?
13. What does `CharGraph.create_app()` create?
14. What does `bind_tools()` do?
15. What does `ToolNode` do?
16. Why does the graph enter knowledge retrieval?
17. Where is the query embedded?
18. What does vector similarity search return?
19. How does a tool result re-enter the Agent?
20. How does an LLM text chunk enter the Queue?
21. How is the same chunk sent toward TTS?
22. Why are TTS bytes encoded as Base64 in SSE?
23. How does `event_stream()` yield SSE events?
24. How does the frontend distinguish content from audio?
25. How does the AI bubble append text incrementally?
26. How does Base64 become bytes again?
27. How does the browser append audio continuously?
28. Where is the completed exchange persisted?
29. Where is token usage stored?
30. What condition triggers memory update?

If you can explain the full path without copying an answer, you have moved from “replicating a project” to **understanding a system**.

---

# 4. Use the same learning loop in every chapter

## Step 1 — State the user need first

Do not begin with:

> I want to learn SSE.

Begin with:

> The user waits ten seconds with no visible answer. I want text to appear while the model is generating.

Technology should emerge from a need.

## Step 2 — Build the simplest version

For chat:

```text
POST → LLM → JSON
```

## Step 3 — Observe the limitation

```text
waiting feels too long
```

## Step 4 — Introduce the next capability

```text
SSE
```

## Step 5 — Observe the new engineering problem

Example:

```text
What happens when JWT expires during a long streaming request?
```

## Step 6 — Extract reusable infrastructure

For example:

```text
streamApi.js
```

That progression is engineering learning, not API memorization.

---

# 5. How to read a real commit

Start with:

```bash
git show --stat <sha>
```

Then inspect the diff:

```bash
git show <sha>
```

Continuously ask:

1. What user/developer problem does this commit solve?
2. Why were these particular files changed?
3. Where does data enter?
4. Where does the result leave?
5. What behavior breaks if the new code disappears?

---

# 6. Recommended commit granularity for your rebuild

Do not make one giant commit for a chapter. For SSE, prefer a sequence such as:

```bash
git commit -m "learn: create basic chat api"
git commit -m "learn: convert chat response to streaming"
git commit -m "learn: emit sse chunks"
git commit -m "learn: receive sse in vue"
git commit -m "learn: append streamed ai text"
```

Your Git history should preserve your reasoning process.

---

# 7. Common learning mistakes

## Mistake 1 — Copy the final code and call it learned

Running code proves the code can run. A stronger test is:

> If the implementation is deleted, can you reconstruct it from the requirement?

## Mistake 2 — Learn every LangChain API first

Learn only what the project currently needs, then expand. In AiFriends the core ideas include Messages, chat models, tools, embeddings, and vector stores.

## Mistake 3 — Start with multi-Agent systems

First understand:

```text
START → agent → END
```

then:

```text
agent → tools → agent
```

Only then move to more complex graphs.

## Mistake 4 — Treat RAG as “a vector database”

A complete RAG path is:

```text
Load
 ↓
Chunk
 ↓
Embedding
 ↓
Store
 ↓
Query Embedding
 ↓
Retrieve
 ↓
Context
 ↓
Generate
```

LanceDB is one storage/retrieval layer inside that pipeline.

---

# 8. Graduation requires your own changes

Do not stop with an exact clone. Add at least three meaningful changes of your own. Useful directions include:

- multiple model/provider adapters;
- structured memory beyond one free-text summary;
- user-uploaded knowledge bases;
- additional permissioned tools;
- production engineering such as PostgreSQL, observability, rate limits, deployment, or stronger tests.

When you do this, preserve the same discipline: requirement → simplest implementation → observed limitation → engineering improvement → tests.

---

# 9. Graduation checklist

## Frontend

- [ ] Understand Vue `ref`, props, and emits
- [ ] Build Router routes
- [ ] Build a Pinia store
- [ ] Call REST APIs
- [ ] Debug in Network tools
- [ ] Handle SSE
- [ ] Understand browser streaming-audio concepts

## Django

- [ ] Explain URL → View → Model
- [ ] Create and apply migrations
- [ ] Use Admin
- [ ] Build APIViews / serializers
- [ ] Explain JWT authorization
- [ ] Query ForeignKey relationships
- [ ] Use `StreamingHttpResponse`

## LangChain

- [ ] Explain System/Human/AI messages
- [ ] Call an OpenAI-compatible chat model
- [ ] Understand token usage
- [ ] Understand embeddings
- [ ] Understand vector stores

## LangGraph

- [ ] Define State
- [ ] Define Nodes
- [ ] Connect Edges
- [ ] Write Conditional Edges
- [ ] Explain `@tool`
- [ ] Explain `bind_tools()`
- [ ] Explain `ToolNode`

## AI application engineering

- [ ] Explain short-term context
- [ ] Explain compressed long-term memory
- [ ] Explain RAG
- [ ] Explain ASR
- [ ] Explain TTS
- [ ] Trace one complete chat data flow
- [ ] Explain how tests/CI protect the maintained implementation

---

# 10. Continue with the maintained learning path

Use these English resources next:

- [English Learning Hub](./README_EN.md)
- [English Quick Start](./QUICK_START_EN.md)
- [English Architecture Guide](./ARCHITECTURE_EN.md)
- [English Troubleshooting Guide](./TROUBLESHOOTING_EN.md)
- [English Labs 00–20](../labs/en/README.md)
- [Bilingual Terminology Guide](./BILINGUAL_GLOSSARY.md)
- [Live Demo Verification](./LIVE_DEMO.md)

Recommended order:

```text
README_EN
  ↓
docs/README_EN.md
  ↓
COURSE_REBUILD_EN.md
  ↓
QUICK_START_EN.md + Labs
  ↓
maintained source code
  ↓
ARCHITECTURE_EN.md
```

The historical commits tell you **how the product grew**. The current Labs, source, tests, and CI tell you **how the project is maintained now**.
