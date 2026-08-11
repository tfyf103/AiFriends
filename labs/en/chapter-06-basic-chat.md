# Chapter 06 Lab: Minimal LLM Chat — Do Not Stream Yet

🌐 **Language:** [简体中文](../chapter-06-basic-chat.md) | **English**

## Goal

Send browser input into a real language model for the first time.

This chapter intentionally does **not** use SSE, tools, long-term memory, RAG, ASR, or TTS.

Build the smallest useful loop first:

```text
Vue input
  ↓ POST JSON
Django chat endpoint
  ↓
LangChain HumanMessage
  ↓
ChatOpenAI-compatible model
  ↓
complete result
  ↓ JSON
Vue displays answer
```

The project’s current runtime supports `AI_MODE=mock`, but this lab is specifically about understanding the boundary where a **real text model** enters the system. Use `AI_MODE=text` only after Mock mode works.

---

## Historical checkpoint

A useful project-history checkpoint is:

```text
72a9866e3370481a8fa6e070e55c7784977c058a  initial chat backend
```

Historical commits are learning material, not guaranteed canonical solutions. Compare them with current code and tests.

---

## TODO 1: Prove the model connection in isolation

Before debugging Vue + Django + auth + model access at the same time, prove the external dependency by itself.

In Django shell or a temporary experiment:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
```

Construct your model using the project’s configured provider settings, then run something equivalent to:

```python
res = llm.invoke([
    HumanMessage('Reply with exactly: connection successful')
])

print(res.content)
```

### Acceptance

- [ ] API credential is accepted.
- [ ] API base/endpoint is correct.
- [ ] chat model name is valid for the provider.
- [ ] `res.content` contains a normal model response.

### Why isolate this first?

If this direct call fails, there is no reason to inspect Vue state or SSE. Reduce the number of possible failure layers.

---

## TODO 2: Switch from Mock to Text mode

After Mock mode is healthy, configure a real text model:

```env
AI_MODE=text
ENABLE_RAG=false
ENABLE_ASR=false
ENABLE_TTS=false

API_KEY=...
API_BASE=...
CHAT_MODEL=...
```

Then run:

```bash
cd backend
python manage.py doctor
```

### Acceptance

- [ ] `doctor` reports the text-mode requirements clearly.
- [ ] You have not enabled RAG or speech yet.

The point is to add **one external dependency class at a time**.

---

## TODO 3: Understand the minimal Chat API contract

The chat endpoint is:

```text
POST /api/friend/message/chat/
```

Conceptual request:

```json
{
  "friend_id": 1,
  "message": "Hello"
}
```

Before worrying about streaming, reason through these checks:

1. `message` must not be empty.
2. `friend_id` must refer to a Friend belonging to the authenticated user.
3. The user text becomes a `HumanMessage`.
4. The backend invokes the chat model.
5. The answer returns to the browser.

### Authorization acceptance

Try changing `friend_id` to another user’s Friend in a controlled test environment.

The backend must reject/not expose that conversation rather than allowing cross-user access.

This is an **object-level authorization** lesson, not an AI lesson.

---

## TODO 4: Build the simplest frontend send flow

At minimum, understand a reactive input such as:

```js
const message = ref('')
```

and a submit handler:

```vue
<form @submit.prevent="handleSend">
```

The flow should include:

```text
trim input
  ↓
empty? return
  ↓
send request
  ↓
show response
```

### Acceptance

- [ ] Pressing Enter can send.
- [ ] Whitespace-only input does not call the backend.
- [ ] A visible error state exists when the request fails.

---

## TODO 5: Record one complete network request

Open browser DevTools → Network and record:

```text
Request URL:
Method:
Authorization header:
Request payload:
Response status:
Response body/content:
Duration:
```

Then answer:

> Why can the browser not display partial AI output while a normal one-shot JSON response is still pending?

Because the response body is treated as a complete result; the browser does not receive application-level answer chunks as they are generated.

That is the motivation for Chapter 07.

---

## TODO 6: Add an artificial delay

Only on your learning branch, temporarily add:

```python
import time
time.sleep(3)
```

before the response returns.

Observe the UI and Network panel.

Answer:

- Is the page actually frozen?
- Is the HTTP request still active?
- Can the user see tokens the model may already have generated?
- What feedback would make this wait feel less ambiguous?

Remove the artificial delay when finished.

---

## TODO 7: Compare “total latency” with “perceived latency”

Measure approximately:

```text
request start
first useful UI feedback
full answer received
```

A non-streaming response may have acceptable total latency but poor perceived latency because time-to-first-visible-output is the entire generation time.

This distinction matters for AI product design.

---

## Reference implementation idea

The conceptual minimum is:

```text
messages = [HumanMessage(message)]
res = llm.invoke(messages)
return JSON/content response
```

Do not add an Agent simply because LangGraph is available.

Understand this progression:

```text
invoke          → stream
JSON            → SSE
single LLM call → LangGraph loop
single turn     → history + memory
no retrieval    → RAG Tool
text only       → optional speech
```

Complexity should enter for a reason.

---

## Common errors

### 401

Inspect JWT/authentication first. This is not a model error.

### 500

Read the Django traceback. Common causes include environment configuration or provider/model failures.

### Provider returns model-not-found / 404

The configured model name may not exist on the selected `API_BASE` provider.

### The returned object looks complicated

LangChain returns Message objects. You usually want:

```python
res.content
```

### Mock works but Text fails

This is useful evidence. Your web/auth/database path is probably healthy; focus on the external model configuration and the code path that builds the real graph/model.

---

## Challenge

Add temporary latency instrumentation for the model call, for example:

```json
{
  "latency_ms": 1234
}
```

or log the timing server-side.

Then answer:

> Are “lower total generation time” and “the product feels faster” the same thing?

Not necessarily. Chapter 07 introduces streaming, which can improve time-to-first-visible-output even when total generation time is similar.

---

Previous: [Chapter 00 — Environment](./chapter-00-environment.md)  
Next: [Chapter 07 — SSE Streaming](./chapter-07-sse.md)
